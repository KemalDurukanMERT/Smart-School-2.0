from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QStyledItemDelegate, QMainWindow, QListWidgetItem, QComboBox, QListWidget, QHeaderView, QMessageBox, QWidget, QCalendarWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
import psycopg2



class MessageApp():
    def __init__(self, data):
        try:
            self.sendMessage.clicked.disconnect()
        except:
            pass
        self.self = data
        self.chattedUser = 0
        self.user = self.self.user
        self.messageCombobox = self.self.findChild(QComboBox, 'messageCombobox')
        self.listView_chats = self.self.listView_chats
        self.listViewMessages = self.self.listViewMessages
        self.sendMessage = self.self.sendMessage
        self.typeMessage = self.self.typeMessage
        self.usermail = self.self.usermail
        self.username = self.self.username
        self.cur = self.self.cur


        self.load_chat_persons()
        self.populateMessageCombobox()

        self.sendMessage.clicked.connect(self.send_message)

        self.messageCombobox.setCurrentIndex(0)
        self.messageCombobox.activated.connect(lambda index: self.chatUser(self.messageCombobox.itemData(index)))

    def read_message(self):

        selected_indexes = self.listView_chats.selectedIndexes()
        for index in selected_indexes:
            item = self.model2.itemFromIndex(index)
            if item:
                item.setBackground(QColor("white"))

    def chatUser(self, user):
        if not user:
            user = 0
        self.chattedUser =  user
        self.cur.execute(f'''
SELECT name, surname, email FROM users WHERE user_id = {user}
''')
       
        data = self.cur.fetchone()
        if data:
            self.username.setText(f'{data[0]} {data[1]}')
            self.usermail.setText(f'{data[2]}')
        else:
            self.username.clear()
            self.usermail.clear()
        
        print(user)
        self.loadMessages(user)
        self.cur.execute(f'''UPDATE message SET message_read = true WHERE receiver_id = {self.user.id} and sender_id = {user}''')

    def send_message(self):
        message_text = self.typeMessage.text()

        try:
            self.cur.execute(f'''
INSERT INTO message (
content, sender_id, receiver_id
) VALUES ('{message_text}', {self.user.id}, {self.chattedUser})
''')
            self.typeMessage.clear()
            self.loadMessages(self.chattedUser)
        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Message Send Error", str(error))
        
        


    def loadMessages(self, user):
        if not user:
            user = 0
        self.cur.execute(f'''SELECT users.name, message.content, message.message_read, message.created_time, message.sender_id FROM
message full JOIN users ON  users.user_id = message.sender_id
WHERE sender_id = {self.user.id} and receiver_id = {user} or sender_id = {user} and receiver_id = {self.user.id}
ORDER BY created_time ASC''')
        
        messages = self.cur.fetchall()
        

        self.model = QStandardItemModel()
        self.listViewMessages.setModel(self.model)
        self.listViewMessages.setItemDelegate(BorderDelegate())

        if messages:
            for name, content, message_read, created_time, sender_id in messages:
                display_text = f'''
    {content}
            {created_time.strftime('%H:%M')}
    '''
                item = QStandardItem(display_text)
                if sender_id == self.user.id:
                    item.setTextAlignment(Qt.AlignRight)
                self.model.appendRow(item)
        
        self.listViewMessages.setModel(self.model)




    def populateMessageCombobox(self):
        self.messageCombobox.clear()
        self.messageCombobox.addItem("Search User for Chat", 0)
        self.cur.execute('''
SELECT user_id, name, surname, email FROM users WHERE status = 'Active'
''')
        users = self.cur.fetchall()
        for user_id, name, surname, email in users:
            display_text = f"{name} - {email}"
            self.messageCombobox.addItem(display_text, user_id)

    def load_chat_persons(self):
        self.model2 = QStandardItemModel()
        self.listView_chats.setModel(self.model2)
        self.cur.execute(f'''
SELECT DISTINCT users.user_id, users.email, users.name
FROM users
JOIN (
    SELECT DISTINCT sender_id AS chat_partner_id
    FROM message
    WHERE receiver_id = {self.user.id}
    UNION
    SELECT DISTINCT receiver_id AS chat_partner_id
    FROM message
    WHERE sender_id = {self.user.id}
) AS chat_partners
ON users.user_id = chat_partners.chat_partner_id; 
''')
        chat_persons = self.cur.fetchall()
        for user_id, email, name in chat_persons:
            self.cur.execute(f'''SELECT users.name, message.content, message.message_read, message.created_time, message.sender_id FROM
message full JOIN users ON  users.user_id = message.sender_id
WHERE sender_id = {user_id} and receiver_id = {self.user.id} and message_read = false''')
            messages = self.cur.fetchall()
            display_text = f"{name} - {email}"
            item = QStandardItem(display_text)
            if messages:
                item.setBackground(QColor('green'))
            item.setData(user_id, Qt.UserRole)
            self.model2.appendRow(item)

        self.listView_chats.clicked.connect(self.on_list_item_clicked)

    def on_list_item_clicked(self, index):
        selected_index = index.row()
        if self.model2.item(selected_index):
            selected_user_id = self.model2.item(selected_index).data(Qt.UserRole)
            self.chatUser(selected_user_id)
            self.read_message()


class BorderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Call the base class paint method
        super(BorderDelegate, self).paint(painter, option, index)

        # Draw a border around the item
        rect = option.rect
        painter.save()
        painter.setPen(Qt.black)
        painter.drawRect(rect)
        painter.restore()