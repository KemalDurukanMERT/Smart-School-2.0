from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QComboBox, QListWidget, QHeaderView, QMessageBox, QWidget, QCalendarWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
import psycopg2
import re
import datetime
from message import *
import sys
import traceback
from validator import *
import hashlib

def exception_hook(exctype, value, tb):
    traceback_details = '\n'.join(traceback.format_tb(tb))
    error_msg = f"Exception type: {exctype}\n"
    error_msg += f"Exception value: {value}\n"
    error_msg += f"Traceback: {traceback_details}"
    QMessageBox.critical(None, 'Unhandled Exception', error_msg)
    sys.exit(1)

sys.excepthook = exception_hook

class AdminApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, cur, database, user):
        super(AdminApp, self).__init__()
        self.setupUi()
        self.connectDatabase(conn, cur, database)
        self.user = user
        self.initializeUi()

    def setupUi(self):
        try:
            loadUi("admin.ui", self)
            self.comboBox_student_a.currentIndexChanged.connect(self.showStudentTodos)
        except Exception as e:
            self.showErrorMessage("Initialization Error", f"Error during TeacherApp initialization: {e}")

    def connectDatabase(self, conn, cur, database):
        self.conn = conn
        self.cur = cur
        self.database = database
        self.populate_students()

    def initializeUi(self):     
        self.setupTabs()
        self.setupMenuActions()
        self.setupButtonActions()
        self.setupCalendar()
        self.setupDeadlineCalendar()
    
    def setupTabs(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)

    def setupMenuActions(self):
        self.menu61_a.triggered.connect(self.add_message_tab)
        self.menu71.triggered.connect(self.logout)
        self.actionAdd_Edit_To_Do_List.triggered.connect(self.showTodoListTab)
        pass

    def setupButtonActions(self):
        pass
    def setupDeadlineCalendar(self):
        self.calendartodo = QCalendarWidget(self)
        self.calendartodo.setWindowFlags(Qt.Popup)
        self.calendartodo.setGridVisible(True)
        self.calendartodo.hide()
        self.calendartodo.clicked.connect(self.updateDeadlineInput)
    def updateDeadlineInput(self, date):
        formatted_date = date.toString("yyyy-MM-dd")
        self.deadline_input_a.setText(formatted_date)
        self.calendar.hide()
    
        
    def onStudentChanged(self, index):
        if index == 0:
            pass  # Placeholder is selected, handle this case separately if needed
        else:
            selected_student = self.comboBox_student_a.currentText()
            self.loadTodos()
        
    def getStudentId(self, student_name):
        
        try:
            query = "SELECT user_id FROM users WHERE CONCAT(name, ' ', surname) = %s"
            self.cur.execute(query, (student_name,))
            result = self.cur.fetchone()
            return result[0] if result else None
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            return None
    
######################################################################################### 
    def showTodoListTab(self):
        self.tabWidget.setCurrentIndex(8)
        # Initialize UI elements for lesson schedule management
        self.deadline_input_a = self.findChild(QLineEdit, 'deadlineInput_a')
        self.todo_name_a = self.findChild(QLineEdit, 'todoName_a')
        # self.task_status = self.findChild(QComboBox, 'task_status')
        self.add_todo_btn_a = self.findChild(QPushButton, 'addTodoBtn_a')
        self.reset_all_todo_fields_btn_a = self.findChild (QPushButton, "resAllTodoFields_a")
        self.delete_todo_btn_a = self.findChild(QPushButton, 'deleteTodoBtn_a')
        self.delete_all_todos_btn_a = self.findChild(QPushButton, 'deleteAllTodosBtn_a')
        self.comboBox_student_a = self.findChild(QComboBox, 'comboBox_student_a')
        self.todo_table_a = self.findChild(QTableWidget, 'todoTable_a')

        
        
        #self.recordsList.itemClicked.connect(self.selectTodo)
        #self.task_status.addItems(['Done', 'Pending'])
        
        self.todo_table_a.setColumnCount(5)
        self.todo_table_a.setHorizontalHeaderLabels(["Task ID","Task", "Deadline", "Status", "Student ID"])
        header = self.todo_table_a.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        self.add_todo_btn_a.clicked.connect(self.addTodo)
        self.deadline_input_a.mousePressEvent = (self.showCalendarTodo)
        self.delete_todo_btn_a.clicked.connect(self.deleteTodo)
        self.delete_all_todos_btn_a.clicked.connect(self.deleteAllTodos)
        self.todo_table_a.itemClicked.connect(self.selectTodo)
        self.allTodosBtn_a.clicked.connect(self.loadTodos)
        self.reset_all_todo_fields_btn_a.clicked.connect ( self.resetAllFieldsTodo)

        # Set column widths
        character_width = 12
        self.todo_table_a.setColumnWidth(0, 10 * character_width)
        self.todo_table_a.setColumnWidth(1, 50 * character_width)
        self.todo_table_a.setColumnWidth(2, 12 * character_width)
        self.todo_table_a.setColumnWidth(3, 12 * character_width)
        self.todo_table_a.setColumnWidth(4, 17 * character_width)
        
        # Fetch and display lessons from the database
        self.loadTodos()
    
    def setupTodoTable(self):
        self.todo_table_a.setHorizontalHeaderLabels(["Task ID", "Task", "Deadline", "Status", "Student"])
        header = self.todo_table_a.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
    
    def loadTodos(self):
        try:
            self.todo_table_a.setRowCount(0)  # Clear the table before repopulating
            query = "SELECT todo_id, task, deadline, task_status, assigned_user_id FROM todolist"
            self.cur.execute(query)
            todos = self.cur.fetchall()
            for todo in todos:
                rowPosition = self.todo_table_a.rowCount()
                self.todo_table_a.insertRow(rowPosition)
                # Inserting items into the table in the correct column order
                self.todo_table_a.setItem(rowPosition, 0, QTableWidgetItem(str(todo[0])))  # Task ID
                self.todo_table_a.setItem(rowPosition, 1, QTableWidgetItem(str(todo[1])))  #  Task
                self.todo_table_a.setItem(rowPosition, 2, QTableWidgetItem(str(todo[2])))  # Deadline
                self.todo_table_a.setItem(rowPosition, 3, QTableWidgetItem(str(todo[3])))  # Status #TODO
                self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem(str(todo[4])))  # Student
            
            # Hide the todo_id column after populating the table
            self.todo_table_a.setColumnHidden(0, True)  # Hides the first column (Task ID)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading todos: {e}')
            
        self.resetAllFieldsTodo()

    def addTodo(self):
        todo_name = self.todo_name_a.text().strip()
        deadline = self.deadline_input_a.text().strip()
        student_name = self.comboBox_student_a.currentText()
        student_id = self.getStudentId(student_name)
        created_by = self.user.id  # Assuming self.user.id holds the ID of the current user

        if not todo_name or not deadline or  student_name is None:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out and a valid instructor must be selected.")
            return

        

        try:
            if self.selected_todo_index is None:  # Add new todo
                query = """
                INSERT INTO todolist (task, deadline, assigned_user_id, created_by)
                VALUES (%s, %s, %s, %s)
                """
                self.cur.execute(query, (todo_name, deadline,  student_id, created_by))
                self.conn.commit()
                QMessageBox.information(self, 'Success', 'Task added successfully')
            else:  # Update existing lesson
                todo_id = self.getTodoIdFromTable(self.selected_todo_index)
                query = """
                UPDATE todolist
                SET task = %s, deadline = %s, assigned_user_id = %s, created_by = %s
                WHERE todo_id = %s
                """
                self.cur.execute(query, (todo_name, deadline,  student_id, created_by, todo_id))
                self.conn.commit()
                QMessageBox.information(self, 'Success', 'Task updated successfully')

            self.loadTodos()  # Reload the tasks to reflect changes
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

        self.resetFormTodo()
        self.selected_todo_index = None  # Reset the selected index
    
    def selectTodo(self, item):
        current_row = item.row()

        todo_name_item = self.todo_table_a.item(current_row, 1)  # todo_name
        deadline_item = self.todo_table_a.item(current_row, 2)  # deadline
        student_item = self.todo_table_a.item(current_row, 4)  # assigned_user_id

        if todo_name_item and deadline_item and student_item:
            self.todo_name_a.setText(todo_name_item.text())
            self.deadline_input_a.setText(deadline_item.text())

            assigned_user_id = int(student_item.text())
            student_name = self.getStudentName(assigned_user_id)
            if student_name:
                student_index = self.comboBox_student_a.findText(student_name, Qt.MatchFixedString)
                if student_index >= 0:
                    self.comboBox_student_a.setCurrentIndex(student_index)

            
            
        else:
            QMessageBox.warning(self, 'Selection Error', 'Failed to retrieve task details.')
        
        self.selected_todo_index = current_row
        

    def showStudentTodos(self):
        selected_student_name = self.comboBox_student_a.currentText()
        if selected_student_name == "Select a Student":
            return  None

        student_id = self.getStudentId(selected_student_name)
        if student_id is None:
            QMessageBox.warning(self, 'Error', 'Selected student ID not found.')
            return

        try:
            self.todo_table_a.setRowCount(0)  # Clear the table before repopulating
            query = "SELECT todo_id, task, deadline, task_status, assigned_user_id FROM todolist WHERE assigned_user_id = %s"
            self.cur.execute(query, (student_id,))
            todos = self.cur.fetchall()
            for todo in todos:
                rowPosition = self.todo_table_a.rowCount()
                self.todo_table_a.insertRow(rowPosition)
                # Inserting items into the table in the correct column order
                self.todo_table_a.setItem(rowPosition, 0, QTableWidgetItem(str(todo[0])))  # Task ID
                self.todo_table_a.setItem(rowPosition, 1, QTableWidgetItem(str(todo[1])))  # Task
                self.todo_table_a.setItem(rowPosition, 2, QTableWidgetItem(str(todo[2])))  # Deadline
                self.todo_table_a.setItem(rowPosition, 3, QTableWidgetItem(str(todo[3])))  # Status
                self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem(str(todo[4])))
            # Hide the todo_id column after populating the table
            self.todo_table_a.setColumnHidden(0, True)  # Hides the first column (Task ID)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading todos: {e}')
    
    def getStudentName(self, assigned_user_id):
        try:
            query = "SELECT CONCAT(name, ' ', surname) FROM users WHERE user_id = %s"
            self.cur.execute(query, (assigned_user_id,))
            result = self.cur.fetchone()

            if result is not None:
                return result[0]
            else:
                # Belirli bir ID'ye sahip öğrenci bulunamadı
                return None
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            return None
        

    def resetAllFieldsTodo ( self ):
        self.todo_name_a.clear()
        self.deadline_input_a.clear()
        self.comboBox_student_a.setCurrentIndex(0)
        
    


    def deleteTodo(self):
        selected_rows = set()
        for item in self.todo_table_a.selectedItems():
            selected_rows.add(item.row())
        for row in sorted(selected_rows, reverse=True):
            todo_id = self.getTodoIdFromTable(row)
            if todo_id:
                try:
                    query = "DELETE FROM todolist WHERE todo_id = %s"
                    self.cur.execute(query, (todo_id,))
                    self.conn.commit()
                    self.todo_table_a.removeRow(row)
                except psycopg2.Error as e:
                    self.conn.rollback()
                    QMessageBox.critical(self, 'Error', f'An error occurred while deleting the todo: {e}')
            else:
                QMessageBox.warning(self, 'Selection Error', 'Could not find the todo ID.')

        self.resetFormTodo()
        self.selected_todo_index = None

    def deleteAllTodos(self):
        try:
            query = "DELETE FROM todolist"
            self.cur.execute(query)
            self.conn.commit()
            self.todo_table_a.setRowCount(0)
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred while deleting all todos: {e}')

        self.resetFormTodo()

    def resetFormTodo(self):
        self.todo_name_a.clear()
        self.deadline_input_a.clear()
        #self.task_status.clear()
        self.comboBox_student_a.setCurrentIndex(0)
        #self.task_status.setCurrentIndex(0)
    
    def getTodoIdFromTable(self, row_index):
        todo_id_item = self.todo_table_a.item(row_index, 0)  # Assuming lesson_id is in the first column
        return int(todo_id_item.text()) if todo_id_item else None

    

    def showCalendarTodo(self, event):
        calendar_pos = self.deadline_input_a.mapToGlobal(self.deadline_input_a.rect().bottomLeft())
        self.calendartodo.move(calendar_pos)
        self.calendartodo.show()
        

    def populate_students(self):
        try:
            self.comboBox_student_a.clear()
            self.comboBox_student_a.addItem("Select a Student")
            students = self.database.get_students(self.cur)
            for  name, surname in students:
                self.comboBox_student_a.addItem(f"{name} {surname}")
        except Exception as e:
            self.showErrorMessage("Database Error", f"Error populating Students: {e}")
    def add_message_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.message_app = MessageApp(self)


    def setupCalendar(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.setGridVisible(True)
        self.calendar.hide()
        self.calendar.clicked.connect(self.updateDateInput)

    def updateDateInput(self, date):
        formatted_date = date.toString("yyyy-MM-dd")
        self.date_input.setText(formatted_date)
        self.calendar.hide()


    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)