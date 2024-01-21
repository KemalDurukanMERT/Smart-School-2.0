import sys
from PyQt5.QtWidgets import QApplication, QListView, QStyledItemDelegate, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


def load_all_persons(conn):
    cursor = conn.cursor()

    command = '''
SELECT email FROM users
'''
    cursor.execute(command)
    return cursor.fetchall()


def load_chat_persons(conn):
    cursor = conn.cursor()

    command = '''

'''


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