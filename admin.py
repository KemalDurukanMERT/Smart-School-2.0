from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QComboBox, QDateEdit, QListWidget, QHeaderView, QMessageBox, QWidget, QCalendarWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
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
from database import *
import os

###############################################################################################################################

def exception_hook(exctype, value, tb):
    traceback_details = '\n'.join(traceback.format_tb(tb))
    error_msg = f"Exception type: {exctype}\n"
    error_msg += f"Exception value: {value}\n"
    error_msg += f"Traceback: {traceback_details}"
    QMessageBox.critical(None, 'Unhandled Exception', error_msg)
    sys.exit(1)

sys.excepthook = exception_hook

###############################################################################################################################
###############################################################################################################################


class AdminApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, cur, database, user):
        super(AdminApp, self).__init__()
        self.setupUi()
        self.connectDatabase(conn, cur, database)
        self.user = user
        self.initializeUi()
        self.pendingUsers()

    def pendingUsers(self):
        self.cur.execute('''
SELECT * FROM users WHERE status = 'Pending'
''')
        users = self.cur.fetchall()
        print(users)
        if users:
            self.menuTeacher.setTitle(f"Users !!({len(users)})!!")
            self.menu12.setText(f"Users !!({len(users)})!!")
        else:
            self.menuTeacher.setTitle(f"Users")
            self.menu12.setText(f"Users")

    def setupUi(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, 'admin.ui')
        try:
            loadUi(ui_path, self)
            
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
        self.selected_todo_index = None
        self.setupMeetingCalendar()
    
    def setupTabs(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)

    def setupMenuActions(self):
        self.menu11.triggered.connect(self.showAddUserTab)
        self.menu12.triggered.connect(self.showEditUserTab)
        self.menu21_t.triggered.connect(self.showLessonScheduleTab)
        self.menu22_t.triggered.connect(self.showLessonAttendanceTab)
        self.menu31_t.triggered.connect(self.showMeetingScheduleTab)
        self.menu32_t.triggered.connect(self.showMeetingAttendanceTab)
        self.actionAdd_Edit_To_Do_List.triggered.connect(self.showTodoListTab)
        self.actionAdd_Edit_Announcement.triggered.connect(self.add_announce_tab)
        self.menu61_a.triggered.connect(self.add_message_tab)
        self.actionCheck_Reports.triggered.connect(self.showReportsTab)
        self.menu71.triggered.connect(self.logout)

        # self.menu61_a.triggered.connect(self.add_message_tab)
        # self.menu71.triggered.connect(self.logout)
        
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
        try:
            self.add_todo_btn_a.clicked.disconnect()
            self.deadline_input_a.clicked.disconnect()
            self.delete_todo_btn_a.clicked.disconnect()
            # self.todo_table_a.itemClicked.connect(self.selectTodo)
            self.allTodosBtn_a.clicked.disconnect()
            self.reset_all_todo_fields_btn_a.clicked.disconnect()
        except:
            pass
        self.tabWidget.setCurrentIndex(8)
        # Initialize UI elements for lesson schedule management
        self.deadline_input_a = self.findChild(QLineEdit, 'deadlineInput_a')
        self.todo_name_a = self.findChild(QLineEdit, 'todoName_a')
        # self.task_status = self.findChild(QComboBox, 'task_status')
        self.add_todo_btn_a = self.findChild(QPushButton, 'addTodoBtn_a')
        self.reset_all_todo_fields_btn_a = self.findChild (QPushButton, "resAllTodoFields_a")
        self.delete_todo_btn_a= self.findChild(QPushButton, 'deleteTodoBtn_a')
        self.delete_all_todos_btn_a = self.findChild(QPushButton, 'deleteAllTodosBtn_a')
        self.comboBox_student_a = self.findChild(QComboBox, 'comboBox_student_a')
        self.todo_table_a = self.findChild(QTableWidget, 'todoTable_a')
        # self.recordsList.itemClicked.connect(self.selectTodo)
        #self.task_status.addItems(['Done', 'Pending'])
        self.todo_table_a.setColumnCount(7)
        self.todo_table_a.setHorizontalHeaderLabels(["Task ID","Task", "Deadline", "Status", "Created By", "Student ID", "Created Id" ])
        header = self.todo_table_a.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        self.add_todo_btn_a.clicked.connect(self.addTodo)
        self.deadline_input_a.mousePressEvent = (self.showCalendarTodo)
        self.delete_todo_btn_a.clicked.connect(self.deleteTodo)
        self.delete_all_todos_btn_a.clicked.connect(self.deleteAllTodos)
        self.todo_table_a.itemClicked.connect(self.selectTodo)
        self.allTodosBtn_a.clicked.connect(self.loadTodos)
        self.reset_all_todo_fields_btn_a.clicked.connect ( self.resetAllFieldsTodo)
        self.comboBox_student_a.currentIndexChanged.connect(self.showStudentTodos)
        # Set column widths
        character_width = 12
        self.todo_table_a.setColumnWidth(0, 10 * character_width)
        self.todo_table_a.setColumnWidth(1, 50 * character_width)
        self.todo_table_a.setColumnWidth(2, 12 * character_width)
        self.todo_table_a.setColumnWidth(3, 12 * character_width)
        self.todo_table_a.setColumnWidth(4, 17 * character_width)
        self.todo_table_a.setColumnWidth(5, 17 * character_width)
        self.todo_table_a.setColumnWidth(6, 17 * character_width)
        # Fetch and display todos from the database
        self.loadTodos()

    def setupTodoTable(self):
        self.todo_table_a.setHorizontalHeaderLabels(["Task ID","Task", "Deadline", "Status", "Created By", "Student ID", "Created Id" ])
        header = self.todo_table_a.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
    
    def loadTodos(self):
        try:
            self.todo_table_a.setRowCount(0)  # Clear the table before repopulating
            query = "SELECT todo_id, task, deadline, task_status, assigned_user_id, created_by FROM todolist"
            self.cur.execute(query)
            todos = self.cur.fetchall()
            for todo in todos:
                rowPosition = self.todo_table_a.rowCount()
                self.todo_table_a.insertRow(rowPosition)
                # Inserting items into the table in the correct column order
                self.todo_table_a.setItem(rowPosition, 0, QTableWidgetItem(str(todo[0])))  # Task ID
                self.todo_table_a.setItem(rowPosition, 1, QTableWidgetItem(str(todo[1])))  #  Task
                self.todo_table_a.setItem(rowPosition, 2, QTableWidgetItem(str(todo[2])))  # Deadline
                self.todo_table_a.setItem(rowPosition, 3, QTableWidgetItem(str(todo[3])))  # Status
                created_by_name = self.getCreatedName(todo[5])
                if created_by_name is not None:
                    self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem(str(created_by_name)))
                else:
                    self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem("Unknown"))
                self.todo_table_a.setItem(rowPosition, 5, QTableWidgetItem(str(todo[4]))) # Student Id
                self.todo_table_a.setItem(rowPosition, 6, QTableWidgetItem(str(todo[5]))) # Created Id
            # Hide the todo_id column after populating the table
            self.todo_table_a.setColumnHidden(0, True)  # Hides the first column (Task ID)
            #self.todo_table.setColumnHidden(5, True)
            self.todo_table_a.setColumnHidden(6, True)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading todos: {e}')
        self.resetAllFieldsTodo()
    def addTodo(self):
        todo_name = self.todo_name_a.text().strip()
        deadline = self.deadline_input_a.text().strip()
        student_name = self.comboBox_student_a.currentText()
        student_id = self.getStudentId(student_name)
        created_by = self.user.id  # Assuming self.user.id holds the ID of the current user
        if not todo_name or not deadline or student_name is None:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out and a valid instructor must be selected.")
            return
        try:
            if self.selected_todo_index is None:  # Add new todo
                query = """
                INSERT INTO todolist (task, deadline, assigned_user_id, created_by)
                VALUES (%s, %s, %s, %s)
                """
                self.cur.execute(query, (todo_name, deadline, student_id, created_by))
                self.conn.commit()
                QMessageBox.information(self, 'Success', 'Task added successfully')
            else:  # Update existing lesson
                todo_id = self.getTodoIdFromTable(self.selected_todo_index)
                query = """
                UPDATE todolist
                SET task = %s, deadline = %s, assigned_user_id = %s, created_by = %s
                WHERE todo_id = %s
                """
                self.cur.execute(query, (todo_name, deadline, student_id, created_by, todo_id))
                self.conn.commit()
                QMessageBox.information(self, 'Success', 'Task updated successfully')
            self.loadTodos()  # Reload the tasks to reflect changes
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            print(e)  # Hata mesajını yazdır
        finally:
            self.resetFormTodo()
            self.selected_todo_index = None  # Reset the selected index
    
    def selectTodo(self, item):
        current_row = item.row()
        todo_name_item = self.todo_table_a.item(current_row, 1)  # todo_name_a
        deadline_item = self.todo_table_a.item(current_row, 2)  # deadline
        student_item = self.todo_table_a.item(current_row, 5)  # assigned_user_id
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
            query = "SELECT todo_id, task, deadline, task_status, assigned_user_id, created_by FROM todolist WHERE assigned_user_id = %s"
            self.cur.execute(query, (student_id,))
            todos = self.cur.fetchall()
            for todo in todos:
                rowPosition = self.todo_table_a.rowCount()
                self.todo_table_a.insertRow(rowPosition)
                # Sadece belirli sütunları ekleyin
                self.todo_table_a.setItem(rowPosition, 0, QTableWidgetItem(str(todo[0])))  # Task Id
                self.todo_table_a.setItem(rowPosition, 1, QTableWidgetItem(str(todo[1])))  # Task
                self.todo_table_a.setItem(rowPosition, 2, QTableWidgetItem(str(todo[2])))  # Deadline
                self.todo_table_a.setItem(rowPosition, 3, QTableWidgetItem(str(todo[3])))# Status
                created_by_name = self.getCreatedName(todo[5])
                if created_by_name is not None:
                    self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem(str(created_by_name)))
                else:
                    self.todo_table_a.setItem(rowPosition, 4, QTableWidgetItem("Unknown"))
                self.todo_table_a.setItem(rowPosition, 5, QTableWidgetItem(str(todo[4])))
                self.todo_table_a.setItem(rowPosition, 6, QTableWidgetItem(str(todo[5])))
            self.todo_table_a.setColumnHidden(0, True)  # Hides the first column (Task ID)
            #self.todo_table_a.setColumnHidden(5, True)
            self.todo_table_a.setColumnHidden(6, True)
        except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while loading todos: {e}')
                
                
                
    def getCreatedName(self, created_by):
        try:
            query = "SELECT CONCAT(name, ' ', surname) FROM users WHERE user_id = %s"
            self.cur.execute(query, (created_by,))
            result = self.cur.fetchone()
            if result is not None:
                return result[0]
            else:
                # Belirli bir ID'ye sahip öğrenci bulunamadı
                return None
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            return None
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
        todo_id_item = self.todo_table_a.item(row_index, 0)  # Assuming todo_id is in the first column
        todo_id = int(todo_id_item.text()) if todo_id_item else None
        if todo_id is None:
            print(f"Todo ID not found in row {row_index}")
        return todo_id
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

 



    
    def setupCalendar(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.setGridVisible(True)
        self.calendar.hide()
        self.calendar.clicked.connect(self.updateDateInput)

    def getInstructorId(self, instructor_name):
        try:
            query = "SELECT user_id FROM users WHERE CONCAT(name, ' ', surname) = %s"
            self.cur.execute(query, (instructor_name,))
            result = self.cur.fetchone()
            return result[0] if result else None
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            return None
        
    def updateDateInput(self, date):
        formatted_date = date.toString("yyyy-MM-dd")
        self.date_input.setText(formatted_date)
        self.calendar.hide() 
###############################################################################################################################

    def add_message_tab(self):
        self.tabWidget.setCurrentIndex(9)
        self.message_app = MessageApp(self)

###############################################################################################################################

# Lesson Schedule Tab   
        
    def showLessonScheduleTab(self):
        try:
            self.add_lesson_btn.clicked.disconnect()
            self.reset_lesson_btn.clicked.disconnect()
            self.delete_lesson_btn.clicked.disconnect()
            self.delete_all_lessons_btn.clicked.disconnect()
        except:
            pass
        self.tabWidget.setCurrentIndex(3)
        # Initialize UI elements for lesson schedule management
        self.selected_lesson_index = None
        self.date_input = self.findChild(QLineEdit, 'dateInput')
        self.lesson_name = self.findChild(QLineEdit, 'lessonName')
        self.time_slot = self.findChild(QLineEdit, 'timeSlot')
        self.add_lesson_btn = self.findChild(QPushButton, 'addLessonBtn')
        self.reset_lesson_btn = self.findChild(QPushButton, 'resetLessonBtn')
        self.delete_lesson_btn = self.findChild(QPushButton, 'deleteLessonBtn')
        self.delete_all_lessons_btn = self.findChild(QPushButton, 'deleteAllLessonsBtn')
        self.comboBox_instructor = self.findChild(QComboBox, 'comboBox_instructor')
        self.lesson_table = self.findChild(QTableWidget, 'lessonTable')

        # self.resetForm()

        self.populate_instructors()

        self.lesson_table.setColumnCount(5)
        self.lesson_table.setHorizontalHeaderLabels(["Lesson ID","Lesson Name", "Date", "Time Slot", "Instructor"])
        header = self.lesson_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        self.add_lesson_btn.clicked.connect(self.addLesson)
        self.reset_lesson_btn.clicked.connect(self.resetForm)
        self.date_input.mousePressEvent = self.showCalendar
        self.delete_lesson_btn.clicked.connect(self.deleteLesson)
        self.delete_all_lessons_btn.clicked.connect(self.deleteAllLessons)
        self.lesson_table.itemClicked.connect(self.selectLesson)

        # Set column widths
        character_width = 12
        self.lesson_table.setColumnWidth(0, 10 * character_width)
        self.lesson_table.setColumnWidth(1, 50 * character_width)
        self.lesson_table.setColumnWidth(2, 12 * character_width)
        self.lesson_table.setColumnWidth(3, 12 * character_width)
        self.lesson_table.setColumnWidth(4, 17 * character_width)
        
        # Fetch and display lessons from the database
        self.loadLessons()
    
    def setupLessonTable(self):
        self.lesson_table.setHorizontalHeaderLabels(["Lesson ID", "Lesson Name", "Date", "Time Slot", "Instructor"])
        header = self.lesson_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
       
    def loadLessons(self):
        try:
            self.lesson_table.setRowCount(0)  # Clear the table before repopulating
            query = "SELECT lesson_id, lesson_name, lesson_date, lesson_time_slot, lesson_instructor FROM lesson ORDER BY lesson_date ASC"
            self.cur.execute(query)
            lessons = self.cur.fetchall()
            for lesson in lessons:
                rowPosition = self.lesson_table.rowCount()
                self.lesson_table.insertRow(rowPosition)
                # Inserting items into the table in the correct column order
                self.lesson_table.setItem(rowPosition, 0, QTableWidgetItem(str(lesson[0])))  # Lesson ID
                self.lesson_table.setItem(rowPosition, 1, QTableWidgetItem(str(lesson[1])))  # Lesson Name
                self.lesson_table.setItem(rowPosition, 2, QTableWidgetItem(str(lesson[2])))  # Date
                self.lesson_table.setItem(rowPosition, 3, QTableWidgetItem(str(lesson[3])))  # Time Slot
                self.lesson_table.setItem(rowPosition, 4, QTableWidgetItem(str(lesson[4])))  # Instructor
            
            # Hide the lesson_id column after populating the table
            self.lesson_table.setColumnHidden(0, True)  # Hides the first column (Lesson ID)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading lessons: {e}')

    def addLesson(self):
        lesson_name = self.lesson_name.text().strip()
        date = self.date_input.text().strip()
        time_slot = self.time_slot.text().strip()
        instructor_name = self.comboBox_instructor.currentText()
        # instructor_id = self.getInstructorId(instructor_name)
        created_by = self.user.id  # Assuming self.user.id holds the ID of the current user
        
        if lesson_name and date and time_slot and instructor_name and instructor_name != "Select an instructor":
            if self.isValidTimeSlot(time_slot):
                if self.selected_lesson_index:
                    lesson_id = self.getLessonIdFromTable(self.selected_lesson_index)
                    query = """
                    UPDATE lesson
                    SET lesson_name = %s, lesson_date = %s, lesson_time_slot = %s, lesson_instructor = %s, created_by = %s
                    WHERE lesson_id = %s
                    """
                    self.cur.execute(query, (lesson_name, date, time_slot, instructor_name, created_by, lesson_id))
                    self.conn.commit()
                    QMessageBox.information(self, 'Success', 'Lesson updated successfully')
                    
                else:
                    query = """
                    INSERT INTO lesson (lesson_name, lesson_date, lesson_time_slot, lesson_instructor, created_by)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    self.cur.execute(query, (lesson_name, date, time_slot, instructor_name, created_by))
                    self.conn.commit()
                    QMessageBox.information(self, 'Success', 'Lesson added successfully')
                    
                self.resetForm()
                self.loadLessons()
                return
            else:
                QMessageBox.warning(self, "Input Error", "Time slot must be in the format xx:xx-xx:xx.")
                
        else:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out and a valid instructor must be selected.")
    
    def selectLesson(self, item):
        print(item)
        current_row = self.lesson_table.row(item)
        print(current_row)
        if current_row >= 0:
            lesson_name_item = self.lesson_table.item(current_row, 1)  # lesson_name
            date_item = self.lesson_table.item(current_row, 2)  # lesson_date
            time_item = self.lesson_table.item(current_row, 3)  # lesson_time_slot
            instructor_item = self.lesson_table.item(current_row, 4)  # lesson_instructor
            
            if lesson_name_item and date_item and time_item and instructor_item:
                self.lesson_name.setText(lesson_name_item.text())
                self.date_input.setText(date_item.text())
                self.time_slot.setText(time_item.text())
                instructor_index = self.comboBox_instructor.findText(instructor_item.text(), Qt.MatchFixedString)
                if instructor_index >= 0:
                    self.comboBox_instructor.setCurrentIndex(instructor_index)
                self.selected_lesson_index = current_row
            else:
                QMessageBox.warning(self, 'Selection Error', 'Failed to retrieve lesson details.')

    def deleteLesson(self):
        selected_rows = set()
        for item in self.lesson_table.selectedItems():
            selected_rows.add(item.row())
        for row in sorted(selected_rows, reverse=True):
            lesson_id = self.getLessonIdFromTable(row)
            if lesson_id:
                try:
                    query = "DELETE FROM lesson WHERE lesson_id = %s"
                    self.cur.execute(query, (lesson_id,))
                    self.conn.commit()
                    self.lesson_table.removeRow(row)
                except psycopg2.Error as e:
                    self.conn.rollback()
                    QMessageBox.critical(self, 'Error', f'An error occurred while deleting the lesson: {e}')
            else:
                QMessageBox.warning(self, 'Selection Error', 'Could not find the lesson ID.')

        self.resetForm()
        self.selected_lesson_index = None

    def deleteAllLessons(self):
        try:
            query = "DELETE FROM lesson"
            self.cur.execute(query)
            self.conn.commit()
            self.lesson_table.setRowCount(0)
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred while deleting all lessons: {e}')

        self.resetForm()

    def resetForm(self):
        self.lesson_name.clear()
        self.date_input.clear()
        self.time_slot.clear()
        self.comboBox_instructor.setCurrentIndex(0)
        # self.selected_lesson_index = None

    def getLessonIdFromTable(self, row_index):
        lesson_id_item = self.lesson_table.item(row_index, 0)  # Assuming lesson_id is in the first column
        return int(lesson_id_item.text()) if lesson_id_item else None

    def showCalendar(self, event):
        calendar_pos = self.date_input.mapToGlobal(self.date_input.rect().bottomLeft())
        self.calendar.move(calendar_pos)
        self.calendar.show()

    def populate_instructors(self):
        try:
            self.comboBox_instructor.clear()
            self.comboBox_instructor.addItem("Select an instructor")
            teachers = self.database.get_teachers(self.cur)
            for name, surname in teachers:
                self.comboBox_instructor.addItem(f"{name} {surname}")
        except Exception as e:
            self.showErrorMessage("Database Error", f"Error populating instructors: {e}")

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

###############################################################################################################################
###############################################################################################################################

# Lesson Attendance Tab   
        
    def showLessonAttendanceTab(self):
        self.tabWidget.setCurrentIndex(4)
        
        # Initialize UI elements for lesson attendance management
        self.lessonComboBox = self.findChild(QComboBox, 'lessonComboBox')
        self.studentComboBox = self.findChild(QComboBox, 'studentComboBox')
        self.statusComboBox = self.findChild(QComboBox, 'statusComboBox')
        self.markAttendanceBtn = self.findChild(QPushButton, 'markAttendanceBtn')
        self.recordsList = self.findChild(QListWidget, 'recordsList')
        
        # Initialize delete buttons
        self.deleteAttendanceBtn = self.findChild(QPushButton, 'deleteAttendanceBtn')
        self.deleteAllAttendanceBtn = self.findChild(QPushButton, 'deleteAllAttendanceBtn')
        self.deleteSelectedStudentAttendanceBtn = self.findChild(QPushButton, 'deleteSelectedStudentAttendanceBtn')

        # Connect buttons to their respective methods
        self.deleteAttendanceBtn.clicked.connect(self.deleteSelectedAttendance)
        self.deleteAllAttendanceBtn.clicked.connect(self.deleteAllAttendance)
        self.deleteSelectedStudentAttendanceBtn.clicked.connect(self.deleteSelectedStudentAttendance)

         # Connect the studentComboBox's signal to the loadAttendanceRecords method
        self.studentComboBox.currentIndexChanged.connect(self.loadAttendanceRecords)

        # Populate combo boxes
        self.populateLessonComboBox()
        self.populateStudentComboBox()

        # Connect the 'Mark Attendance' button click to the method
        self.markAttendanceBtn.clicked.connect(self.markAttendance)
        
        # Connect the itemClicked signal to the populateFields method
        self.recordsList.itemClicked.connect(self.populateFields)
        
        # Clear existing items in recordsList and reset combo boxes
        self.recordsList.clear()
        self.lessonComboBox.setCurrentIndex(0)
        self.studentComboBox.setCurrentIndex(0)
        self.statusComboBox.setCurrentIndex(0)
        
        # Initialize statusComboBox with placeholder and options
        self.statusComboBox.clear()  # Clear existing items
        self.statusComboBox.addItem("Please select a status...")  # Add placeholder text
        for status in ['Present', 'Absent', 'Late', 'Excused']:
            self.statusComboBox.addItem(status)

    def populateLessonComboBox(self):
        self.lessonComboBox.clear()  # Clear existing items
        font = self.lessonComboBox.font()  # Get the current font
        font.setPointSize(12)  # Set the font size
        self.lessonComboBox.setFont(font)  # Apply the font
        
        self.lessonComboBox.addItem("Please select a lesson...")  # Add placeholder text
        self.cur.execute("SELECT lesson_id, lesson_name, lesson_date, lesson_time_slot FROM lesson")
        lessons = self.cur.fetchall()
        for lesson_id, lesson_name, lesson_date, lesson_time_slot in lessons:
            display_text = f"{lesson_name} - {lesson_date} - {lesson_time_slot}"
            self.lessonComboBox.addItem(display_text, lesson_id)

    def populateStudentComboBox(self):
        self.studentComboBox.clear()  # Clear existing items
        font = self.studentComboBox.font()  # Get the current font
        font.setPointSize(12)  # Set the font size
        self.studentComboBox.setFont(font)  # Apply the font
        
        self.studentComboBox.addItem("Please select a student...")  # Add placeholder text
        self.cur.execute("SELECT user_id, name, surname, email FROM users WHERE user_type = 'student'")
        students = self.cur.fetchall()
        for user_id, name, surname, email in students:
            display_text = f"{name} {surname} - {email}"
            self.studentComboBox.addItem(display_text, user_id)

    def loadAttendanceRecords(self):
        self.recordsList.clear()  # Clear existing items
        self.recordsList.setFont(QtGui.QFont("Courier New", 12))  # Set monospaced font
        
        user_id = self.studentComboBox.currentData()
        if user_id:
            try:
                query = """
                SELECT la.attendance_id, l.lesson_name, l.lesson_date, l.lesson_time_slot, la.status
                FROM lessonattendance la
                JOIN lesson l ON la.lesson_id = l.lesson_id
                WHERE la.user_id = %s
                """
                self.cur.execute(query, (user_id,))
                records = self.cur.fetchall()
                for attendance_id, lesson_name, lesson_date, lesson_time_slot, status in records:
                    # Convert lesson_date to string if it's a date object (adjust format as needed)
                    lesson_date_str = lesson_date.strftime("%Y-%m-%d") if isinstance(lesson_date, datetime.date) else lesson_date
                    record_text = f"Lesson: {lesson_name:40s} Date: {lesson_date_str:10s}  Time: {lesson_time_slot:13s}  Status: {status.capitalize():10s}"
                    listItem = QListWidgetItem(record_text)
                    listItem.setData(Qt.UserRole, attendance_id)  # Storing attendance_id as user data
                    self.recordsList.addItem(listItem)
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
               
    def markAttendance(self):
        lesson_id = self.lessonComboBox.currentData()
        user_id = self.studentComboBox.currentData()
        status = self.statusComboBox.currentText().lower()  # Convert status to lowercase
        created_by = self.user.id  # Assuming self.user.id holds the ID of the current user

        if not lesson_id or self.lessonComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid lesson.")
            return
        if not user_id or self.studentComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid student.")
            return
        if not status or self.statusComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid status.")
            return

        try:
            # Check if an attendance record already exists for the selected student and lesson
            query = """
            SELECT attendance_id FROM lessonattendance
            WHERE user_id = %s AND lesson_id = %s
            """
            self.cur.execute(query, (user_id, lesson_id))
            existing_record = self.cur.fetchone()

            if existing_record:  # Record exists, so update it
                attendance_id = existing_record[0]
                query = """
                UPDATE lessonattendance
                SET status = %s, created_by = %s
                WHERE attendance_id = %s
                """
                self.cur.execute(query, (status, created_by, attendance_id))
            else:  # No existing record, insert new
                query = """
                INSERT INTO lessonattendance (user_id, lesson_id, status, created_by)
                VALUES (%s, %s, %s, %s)
                """
                self.cur.execute(query, (user_id, lesson_id, status, created_by))
            
            self.conn.commit()
            self.loadAttendanceRecords()  # Reload the attendance records
            QMessageBox.information(self, 'Success', 'Attendance record updated successfully' if existing_record else 'Attendance marked successfully')
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {e}')   

    def populateFields(self, item):
        attendance_id = item.data(Qt.UserRole)  # Retrieve the attendance_id directly from the item's user data
        if attendance_id:
            try:
                # Query to fetch the attendance record details based on attendance_id
                query = """
                SELECT la.user_id, la.lesson_id, la.status
                FROM lessonattendance la
                WHERE la.attendance_id = %s
                """
                self.cur.execute(query, (attendance_id,))
                record = self.cur.fetchone()
                if record:
                    user_id, lesson_id, status = record
                    
                    # Find and set the index of the studentComboBox based on user_id
                    index = self.studentComboBox.findData(user_id)
                    if index >= 0:
                        self.studentComboBox.setCurrentIndex(index)
                    
                    # Find and set the index of the lessonComboBox based on lesson_id
                    index = self.lessonComboBox.findData(lesson_id)
                    if index >= 0:
                        self.lessonComboBox.setCurrentIndex(index)
                    
                    # Find and set the index of the statusComboBox based on status
                    index = self.statusComboBox.findText(status, Qt.MatchFixedString)
                    if index >= 0:
                        self.statusComboBox.setCurrentIndex(index)
                else:
                    QMessageBox.warning(self, 'Not Found', 'Attendance record not found.')
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')            
    
    def deleteSelectedAttendance(self):
        selected_items = self.recordsList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'Please select an attendance record to delete.')
            return

        for item in selected_items:
            attendance_id = item.data(Qt.UserRole)  # Retrieve the attendance_id directly from the item's user data
            if attendance_id is None:
                QMessageBox.warning(self, 'Selection Error', 'Failed to retrieve attendance ID.')
                continue

            try:
                query = "DELETE FROM lessonattendance WHERE attendance_id = %s"
                self.cur.execute(query, (attendance_id,))
                self.conn.commit()
                # Remove the item from the QListWidget
                self.recordsList.takeItem(self.recordsList.row(item))
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
                self.conn.rollback()

        # Reload the attendance records to reflect the changes
        self.loadAttendanceRecords()

    def deleteSelectedStudentAttendance(self):
        user_id = self.studentComboBox.currentData()
        if not user_id:
            QMessageBox.warning(self, "Selection Error", "Please select a student.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete all attendance records for the selected student?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM lessonattendance WHERE user_id = %s"
                self.cur.execute(query, (user_id,))
                self.conn.commit()
                self.loadAttendanceRecords()  # Reload the attendance records to reflect the changes
                QMessageBox.information(self, 'Success', 'All attendance records for the selected student have been deleted.')
            except psycopg2.Error as e:
                self.conn.rollback()
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

    def deleteAllAttendance(self):
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete all attendance records?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM lessonattendance"
                self.cur.execute(query)
                self.conn.commit()
                # Clear all items from the QListWidget
                self.recordsList.clear()
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
                self.conn.rollback()

    def parseAttendanceId(self, record_text):
        # Extract the attendance_id from the record_text
        try:
            # Assuming the attendance_id is stored as user data in the QListWidgetItem
            return int(record_text)
        except (ValueError):
            QMessageBox.critical(self, 'Error', 'Failed to parse attendance ID.')
            return None

###############################################################################################################################
###############################################################################################################################
      
# Meeting Schedule Tab   
    def showMeetingScheduleTab(self):
        try:
            self.add_meeting_btn.clicked.disconnect()
        except:
            pass
        try:
            self.tabWidget.setCurrentIndex(5)
            
            # Find or create UI elements for meeting schedule management
            self.meeting_date_input = self.findChild(QLineEdit, 'meetingDateInput')
            self.meeting_title = self.findChild(QLineEdit, 'meetingTitle')
            self.meeting_time_slot = self.findChild(QLineEdit, 'meetingTimeSlot')
            self.add_meeting_btn = self.findChild(QPushButton, 'addMeetingBtn')
            self.reset_meeting_btn = self.findChild(QPushButton, 'resetMeetingBtn')
            self.delete_meeting_btn = self.findChild(QPushButton, 'deleteMeetingBtn')
            self.delete_all_meetings_btn = self.findChild(QPushButton, 'deleteAllMeetingsBtn')
            self.meeting_table = self.findChild(QTableWidget, 'meetingTable')

            # Initialize the meeting table
            self.meeting_table.setColumnCount(3)
            self.meeting_table.setHorizontalHeaderLabels(["Meeting Title", "Meeting Date", "Meeting Time"])
            header = self.meeting_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            self.meeting_table.setSelectionBehavior(QTableWidget.SelectRows)
            
            # Connect buttons to their respective functions
            self.add_meeting_btn.clicked.connect(self.addMeeting)
            self.reset_meeting_btn.clicked.connect(self.resetMeetingButton)
            self.meeting_date_input.mousePressEvent = self.showMeetingCalendar
            self.delete_meeting_btn.clicked.connect(self.deleteMeeting)
            self.delete_all_meetings_btn.clicked.connect(self.deleteAllMeetings)
            self.meeting_table.itemClicked.connect(self.selectMeeting)
            
            # Set column widths
            character_width = 12
            self.meeting_table.setColumnWidth(0, 35 * character_width)
            self.meeting_table.setColumnWidth(1, 12 * character_width)
            self.meeting_table.setColumnWidth(2, 12 * character_width)
            
            # Load meetings from the database
            self.loadMeetings()
            
            self.selected_meeting_index = None  # Initialize the selected meeting index
            # self.loadMeetings()
        except Exception as e:
            print(f"Error in showMeetingScheduleTab: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred in showMeetingScheduleTab: {str(e)}")

    def setupMeetingCalendar(self):
        self.meeting_calendar = QCalendarWidget(self)
        self.meeting_calendar.setWindowFlags(Qt.Popup)
        self.meeting_calendar.setGridVisible(True)
        self.meeting_calendar.hide()
        self.meeting_calendar.clicked.connect(self.updateMeetingDateInput)

    def updateMeetingDateInput(self, date):
        formatted_meeting_date = date.toString("yyyy-MM-dd")
        self.meeting_date_input.setText(formatted_meeting_date)
        self.meeting_calendar.hide()

    def isValidTimeSlot(self, time_slot):
        pattern = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
        return re.match(pattern, time_slot)

    def showMeetingCalendar(self, event):
        meeting_calendar_pos = self.meeting_date_input.mapToGlobal(self.meeting_date_input.rect().bottomLeft())
        self.meeting_calendar.move(meeting_calendar_pos)
        self.meeting_calendar.show()
          
    def selectMeeting(self, item):
        current_row = self.meeting_table.row(item)
        if current_row >= 0:
            meeting_item = self.meeting_table.item(current_row, 0)
            date_item = self.meeting_table.item(current_row, 1)
            time_item = self.meeting_table.item(current_row, 2)
            if meeting_item and date_item and time_item:
                meeting_name = meeting_item.text()
                date = date_item.text()
                time = time_item.text()
                self.meeting_title.setText(meeting_name)
                self.meeting_date_input.setText(date)
                self.meeting_time_slot.setText(time)
                self.selected_meeting_index = current_row
            else:
                print("Some items are None!")

    def loadMeetings(self):
        self.meeting_table.clearContents()
        self.meeting_table.setRowCount(0)
        query = "SELECT meeting_id, meeting_name, meeting_date, meeting_time_slot FROM meeting ORDER BY meeting_date ASC"
        self.cur.execute(query, (self.user.id,))
        meetings = self.cur.fetchall()
        for meeting_id, meeting_name, meeting_date, meeting_time_slot in meetings:
            rowPosition = self.meeting_table.rowCount()
            self.meeting_table.insertRow(rowPosition)
            self.meeting_table.setItem(rowPosition, 0, QTableWidgetItem(meeting_name))
            # Format meeting_date as a string in the format "yyyy-MM-dd"
            meeting_date_str = meeting_date.strftime("%Y-%m-%d") if isinstance(meeting_date, datetime.date) else meeting_date
            self.meeting_table.setItem(rowPosition, 0, QTableWidgetItem(meeting_name))
            self.meeting_table.setItem(rowPosition, 1, QTableWidgetItem(meeting_date_str))
            self.meeting_table.setItem(rowPosition, 2, QTableWidgetItem(meeting_time_slot))
            # Set meeting_id as user data for the first column's item
            self.meeting_table.item(rowPosition, 0).setData(Qt.UserRole, meeting_id)

    def addMeeting(self):
        title = self.meeting_title.text().strip()
        date = self.meeting_date_input.text().strip()
        time = self.meeting_time_slot.text().strip()
        created_by = self.user.id

        if not title or not date or not time:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        if not self.isValidTimeSlot(time):
            QMessageBox.warning(self, "Input Error", "Time slot must be in the format xx:xx-xx:xx.")
            return

        try:
            if self.selected_meeting_index is not None:
                meeting_id = self.meeting_table.item(self.selected_meeting_index, 0).data(Qt.UserRole)
                query = "UPDATE meeting SET meeting_name = %s, meeting_date = %s, meeting_time_slot = %s, created_by = %s WHERE meeting_id = %s"
                self.cur.execute(query, (title, date, time, created_by, meeting_id))
            else:
                query = "INSERT INTO meeting (meeting_name, meeting_date, meeting_time_slot, teacher_id, created_by) VALUES (%s, %s, %s, %s, %s)"
                self.cur.execute(query, (title, date, time, self.user.id, created_by))
            
            self.conn.commit()
            self.loadMeetings()
            QMessageBox.information(self, 'Success', 'Meeting updated successfully' if self.selected_meeting_index is not None else 'Meeting added successfully')
        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
        self.meeting_title.clear()
        self.meeting_date_input.clear()
        self.meeting_time_slot.clear()
        self.selected_meeting_index = None  # Reset the selected meeting index

    def resetMeetingButton(self):
        self.meeting_title.clear()
        self.meeting_date_input.clear()
        self.meeting_time_slot.clear()
        self.selected_meeting_index = None

    def deleteMeeting(self):
        selected_rows = set()
        for item in self.meeting_table.selectedItems():
            selected_rows.add(item.row())
        for row in sorted(selected_rows, reverse=True):
            meeting_id = self.meeting_table.item(row, 0).data(Qt.UserRole)
            if meeting_id:
                try:
                    query = "DELETE FROM meeting WHERE meeting_id = %s"
                    self.cur.execute(query, (meeting_id,))
                    self.conn.commit()
                except Exception as e:
                    self.conn.rollback()
                    QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.meeting_table.removeRow(row)

        # Clear the line edits
        self.meeting_title.clear()
        self.meeting_date_input.clear()
        self.meeting_time_slot.clear()
        self.selected_meeting_index = None  # Reset the selected meeting index

    def deleteAllMeetings(self):
        try:
            query = "DELETE FROM meeting WHERE teacher_id = %s"
            self.cur.execute(query, (self.user.id,))
            self.conn.commit()
            self.loadMeetings()
            QMessageBox.information(self, 'Success', 'All meetings have been deleted.')
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

        # Clear the line edits
        self.meeting_title.clear()
        self.meeting_date_input.clear()
        self.meeting_time_slot.clear()
        self.selected_meeting_index = None  # Reset the selected meeting index

    def selectMeeting(self, item):
        current_row = self.meeting_table.row(item)
        if current_row >= 0:
            title_item = self.meeting_table.item(current_row, 0)
            date_item = self.meeting_table.item(current_row, 1)
            time_item = self.meeting_table.item(current_row, 2)
            if title_item and date_item and time_item:
                title = title_item.text()
                date = date_item.text()
                time = time_item.text()
                self.meeting_title.setText(title)
                self.meeting_date_input.setText(date)
                self.meeting_time_slot.setText(time)
                self.selected_meeting_index = current_row
            else:
                QMessageBox.warning(self, "Selection Error", "Failed to retrieve meeting details.")

###############################################################################################################################
###############################################################################################################################

# Meeting Attendance Tab   
    
    def showMeetingAttendanceTab(self):
        self.tabWidget.setCurrentIndex(6)
            
        # Initialize UI elements for meeting attendance management
        self.meetingComboBox = self.findChild(QComboBox, 'meetingComboBox_3')
        self.studentComboBox = self.findChild(QComboBox, 'studentComboBox_4')
        self.statusComboBox = self.findChild(QComboBox, 'statusComboBox_4')
        self.markAttendanceBtn = self.findChild(QPushButton, 'markAttendanceBtn_4')
        self.recordsList = self.findChild(QListWidget, 'recordsList_4')
            
        # Initialize delete buttons
        self.deleteAttendanceBtn = self.findChild(QPushButton, 'deleteAttendanceBtn_4')
        self.deleteAllAttendanceBtn = self.findChild(QPushButton, 'deleteAllAttendanceBtn_4')
        self.deleteSelectedStudentAttendanceBtn = self.findChild(QPushButton, 'deleteSelectedStudentAttendanceBtn_4')
        # Connect buttons to their respective methods
        self.deleteAttendanceBtn.clicked.connect(self.deleteSelectedMeetingAttendance)
        self.deleteAllAttendanceBtn.clicked.connect(self.deleteAllMeetingAttendance)
        self.deleteSelectedStudentAttendanceBtn.clicked.connect(self.deleteSelectedStudentMeetingAttendance)
            
        # Connect the studentComboBox's signal to the loadAttendanceRecords method
        self.studentComboBox.currentIndexChanged.connect(self.loadMeetingAttendanceRecords)

        # Populate combo boxes
        self.populateMeetingComboBox()
        self.populateStudentComboBox()

        # Connect the 'Mark Attendance' button click to the method
        self.markAttendanceBtn.clicked.connect(self.markMeetingAttendance)
            
        # Connect the itemClicked signal to the populateFields method
        self.recordsList.itemClicked.connect(self.populateMeetingFields)
            
        # Clear existing items in recordsList and reset combo boxes
        self.recordsList.clear()
        self.meetingComboBox.setCurrentIndex(0)
        self.studentComboBox.setCurrentIndex(0)
        self.statusComboBox.setCurrentIndex(0)
            
        # Initialize statusComboBox with placeholder and options
        self.statusComboBox.clear()  # Clear existing items
        self.statusComboBox.addItem("Please select a status...")  # Add placeholder text
        for status in ['Present', 'Absent', 'Late']:
            self.statusComboBox.addItem(status)    

    def populateMeetingComboBox(self):
        self.meetingComboBox.clear()  # Clear existing items
        font = self.meetingComboBox.font()  # Get the current font
        font.setPointSize(12)  # Set the font size
        self.meetingComboBox.setFont(font)  # Apply the font
        
        self.meetingComboBox.addItem("Please select a meeting...")  # Add placeholder text
        
        self.cur.execute("SELECT meeting_id, meeting_name, meeting_date, meeting_time_slot FROM meeting")
        meetings = self.cur.fetchall()
        for meeting_id, meeting_name, meeting_date, meeting_time_slot in meetings:
            display_text = f"{meeting_name} - {meeting_date} - {meeting_time_slot}"
            self.meetingComboBox.addItem(display_text, meeting_id)
            
    def populateStudentComboBox(self):
        self.studentComboBox.clear()  # Clear existing items
        font = self.studentComboBox.font()  # Get the current font
        font.setPointSize(12)  # Set the font size
        self.studentComboBox.setFont(font)  # Apply the font
        
        self.studentComboBox.addItem("Please select a student...")  # Add placeholder text
        self.cur.execute("SELECT user_id, name, surname, email FROM users WHERE user_type = 'student'")
        students = self.cur.fetchall()
        for user_id, name, surname, email in students:
            display_text = f"{name} {surname} - {email}"
            self.studentComboBox.addItem(display_text, user_id)        
              
    def loadMeetingAttendanceRecords(self):
        self.recordsList.clear()  # Clear existing items
        self.recordsList.setFont(QtGui.QFont("Courier New", 12))  # Set monospaced font

        
        user_id = self.studentComboBox.currentData()
        if user_id:
            try:
                query = """
                SELECT ma.attendance_id, m.meeting_name, m.meeting_date, m.meeting_time_slot, ma.status
                FROM meetingattendance ma
                JOIN meeting m ON ma.meeting_id = m.meeting_id
                WHERE ma.user_id = %s
                """
                self.cur.execute(query, (user_id,))
                records = self.cur.fetchall()
                for attendance_id, meeting_name, meeting_date, meeting_time_slot, status in records:
                    # Convert lesson_date to string if it's a date object (adjust format as needed)
                    meeting_date_str = meeting_date.strftime("%Y-%m-%d") if isinstance(meeting_date, datetime.date) else meeting_date
                    
                    record_text = f"Meeting: {meeting_name:40s} Date: {meeting_date_str:10s} Time: {meeting_time_slot:13s} Status: {status.capitalize():10s}"
                    listItem = QListWidgetItem(record_text)
                    listItem.setData(Qt.UserRole, attendance_id)  # Storing attendance_id as user data
                    self.recordsList.addItem(listItem)
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

    def markMeetingAttendance(self):
        meeting_id = self.meetingComboBox.currentData()
        user_id = self.studentComboBox.currentData()
        status = self.statusComboBox.currentText().lower()  # Convert status to lowercase
        created_by = self.user.id  # Assuming self.user.id holds the ID of the current user

        if not meeting_id or self.meetingComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid meeting.")
            return
        if not user_id or self.studentComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid student.")
            return
        if not status or self.statusComboBox.currentIndex() == 0:
            QMessageBox.warning(self, "Input Error", "Please select a valid status.")
            return

        try:
            query = """
            SELECT attendance_id FROM meetingattendance
            WHERE user_id = %s AND meeting_id = %s
            """
            self.cur.execute(query, (user_id, meeting_id))
            existing_record = self.cur.fetchone()

            if existing_record:
                attendance_id = existing_record[0]
                query = """
                UPDATE meetingattendance
                SET status = %s, created_by = %s
                WHERE attendance_id = %s
                """
                self.cur.execute(query, (status, created_by, attendance_id))
            else:
                query = """
                INSERT INTO meetingattendance (user_id, meeting_id, status, created_by)
                VALUES (%s, %s, %s, %s)
                """
                self.cur.execute(query, (user_id, meeting_id, status, created_by))
            
            self.conn.commit()
            self.loadMeetingAttendanceRecords()  # Reload the attendance records
            QMessageBox.information(self, 'Success', 'Attendance record updated successfully' if existing_record else 'Attendance marked successfully')
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An unexpected error occurred: {e}')

    def populateMeetingFields(self, item):
        attendance_id = item.data(Qt.UserRole)  # Retrieve the attendance_id directly from the item's user data
        if attendance_id:
                try:
                    query = """
                    SELECT ma.user_id, ma.meeting_id, ma.status
                    FROM meetingattendance ma
                    WHERE ma.attendance_id = %s
                    """
                    self.cur.execute(query, (attendance_id,))
                    record = self.cur.fetchone()
                    if record:
                        user_id, meeting_id, status = record
                        index = self.studentComboBox.findData(user_id)
                        if index >= 0:
                            self.studentComboBox.setCurrentIndex(index)
                        index = self.meetingComboBox.findData(meeting_id)
                        if index >= 0:
                            self.meetingComboBox.setCurrentIndex(index)
                        index = self.statusComboBox.findText(status, Qt.MatchFixedString)
                        if index >= 0:
                            self.statusComboBox.setCurrentIndex(index)
                    else:
                        QMessageBox.warning(self, 'Not Found', 'Attendance record not found.')
                        
                except psycopg2.Error as e:
                    QMessageBox.critical(self, 'Error', f'An error occurred: {e}')    

    # Methods for deleting attendance records (deleteSelectedMeetingAttendance, deleteAllMeetingAttendance, deleteSelectedStudentMeetingAttendance) should be similarly adjusted for meeting attendance.

    def deleteSelectedMeetingAttendance(self):
        selected_items = self.recordsList.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'Please select a meeting attendance record to delete.')
            return

        for item in selected_items:
            attendance_id = item.data(Qt.UserRole)  # Retrieve the attendance_id directly from the item's user data
            if attendance_id is None:
                QMessageBox.warning(self, 'Selection Error', 'Failed to retrieve attendance ID.')
                continue

            try:
                query = "DELETE FROM meetingattendance WHERE attendance_id = %s"
                self.cur.execute(query, (attendance_id,))
                self.conn.commit()
                # Remove the item from the QListWidget
                self.recordsList.takeItem(self.recordsList.row(item))
            except psycopg2.Error as e:
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
                self.conn.rollback()

        # Reload the attendance records to reflect the changes
        self.loadMeetingAttendanceRecords()

    def deleteSelectedStudentMeetingAttendance(self):
        user_id = self.studentComboBox.currentData()
        if not user_id:
            QMessageBox.warning(self, "Selection Error", "Please select a student.")
            return

        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete all meeting attendance records for the selected student?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM meetingattendance WHERE user_id = %s"
                self.cur.execute(query, (user_id,))
                self.conn.commit()
                self.loadMeetingAttendanceRecords()  # Reload the attendance records to reflect the changes
                QMessageBox.information(self, 'Success', 'All meeting attendance records for the selected student have been deleted.')
            except psycopg2.Error as e:
                self.conn.rollback()
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')
            
    def deleteAllMeetingAttendance(self):
        reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete all meeting attendance records?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM meetingattendance"
                self.cur.execute(query)
                self.conn.commit()
                # Clear all items from the QListWidget
                self.recordsList.clear()
            except psycopg2.Error as e:
                self.conn.rollback()
                QMessageBox.critical(self, 'Error', f'An error occurred: {e}')   
                
    def parseAttendanceId(self, record_text):
        # Extract the attendance_id from the record_text
        try:
            # Assuming the attendance_id is stored as user data in the QListWidgetItem
            return int(record_text)
        except (ValueError):
            QMessageBox.critical(self, 'Error', 'Failed to parse attendance ID.')
            return None     
        
###############################################################################################################################
###############################################################################################################################
    def showAddUserTab(self):
        try:
            self.b5.clicked.disconnect()
        except:
            pass
        self.b5.clicked.connect(self.registerAsAdmin)
        self.cb21_5.currentIndexChanged.connect(self.on_status_change)
        self.cb21_4.currentIndexChanged.connect(self.on_usertype_change)
        self.tabWidget.setCurrentIndex(1)

    def registerAsAdmin(self):
        email = self.tb12.text()
        name = self.tb13.text()
        surname = self.tb14.text()
        city = self.tb15.text()
        phone = self.tb16.text()
        password = self.tb17.text()

        cur = self.conn.cursor()

        if not is_valid_email(email) or not is_valid_password(password) or not is_valid_phone(phone):
            QMessageBox.warning(self, "Registration Error", "Invalid input format")
            return

        password = self.hash_password(password)

        try:
            command = '''
            INSERT INTO users (email, hashed_password, name, surname, phone, city, user_type, status, created_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            '''
            cur.execute(command, (email, password, name, surname, phone, city, self.addUserType, self.addUserStatus))

            cur.close()

            self.conn.commit()

            QMessageBox.information(self, "Registration Successful", "Account created successfully")

            self.resetAdminRegisterForm()

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Registration Error", f"{error}")

    def resetAdminRegisterForm(self):
        self.tb12.clear()
        self.tb13.clear()
        self.tb14.clear()
        self.tb15.clear()
        self.tb16.clear()
        self.tb17.clear()
        self.cb21_5.setCurrentIndex(-1)
        self.cb21_4.setCurrentIndex(-1)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def on_status_change(self):
        self.addUserStatus = self.cb21_5.currentText()
    def on_usertype_change(self):
        self.addUserType = self.cb21_4.currentText()


    def showEditUserTab(self):
        self.pendingUsers()
        try:
            self.saveUserDetails.clicked.disconnect()
            self.deleteUserDetails.clicked.disconnect()
        except:
            pass

        self.tabWidget.setCurrentIndex(2)
        # self.userCombobox = self.findChild(QComboBox, 'cb21')
        self.statusCombobox = self.findChild(QComboBox, 'cb21_3')
        self.typeCombobox = self.findChild(QComboBox, 'cb21_2')
        self.tableStatusCombobox = self.findChild(QComboBox, 'cb21_6')
        self.emailEdit = self.findChild(QLineEdit, 'tb22')
        self.nameEdit = self.findChild(QLineEdit, 'tb23')
        self.surnameEdit = self.findChild(QLineEdit, 'tb24')
        self.cityEdit = self.findChild(QLineEdit, 'tb25')
        self.phoneEdit = self.findChild(QLineEdit, 'tb26')
        self.passwordEdit = self.findChild(QLineEdit, 'tb27')
        self.editUserTable = self.findChild(QTableWidget, 'users_table')
        self.saveUserDetails = self.findChild(QPushButton, 'b6')
        self.deleteUserDetails = self.findChild(QPushButton, 'b7')

        self.statusCombobox.setCurrentIndex(-1)
        self.typeCombobox.setCurrentIndex(-1)
        self.tableStatusCombobox.setCurrentIndex(0)
        self.emailEdit.clear()
        self.nameEdit.clear()
        self.surnameEdit.clear()
        self.cityEdit.clear()
        self.phoneEdit.clear()
        self.passwordEdit.clear()
        self.tableStatusCombobox.currentIndexChanged.connect(self.changeTableStatus)
        self.statusCombobox.currentIndexChanged.connect(self.changeStatusCb)
        self.typeCombobox.currentIndexChanged.connect(self.changeTypeCb)



        self.editUserTable.setColumnCount(4)
        self.editUserTable.setHorizontalHeaderLabels(["User Email", "Name", "Surname", "Status"])
        header = self.editUserTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        
        self.tableStatus = 'Pending'
        self.loadUserForAdmin()

        self.editUserTable.itemClicked.connect(self.selectEditUser)
        self.saveUserDetails.clicked.connect(self.saveDetail)
        self.deleteUserDetails.clicked.connect(self.deleteDetail)
        
        # Set column widths
        character_width = 12
        self.users_table.setColumnWidth(0, 25 * character_width)
        self.users_table.setColumnWidth(1, 11 * character_width)
        self.users_table.setColumnWidth(2, 11 * character_width)
        self.users_table.setColumnWidth(3, 11 * character_width)

    def changeStatusCb(self):
        self.editUserStatus = self.statusCombobox.currentText()
    def changeTypeCb(self):
        self.editUserType = self.typeCombobox.currentText()

    def saveDetail(self):
        status = self.editUserStatus
        type = self.editUserType
        email = self.emailEdit.text()
        name = self.nameEdit.text()
        surname = self.surnameEdit.text()
        city = self.cityEdit.text()
        phone = self.phoneEdit.text()
        password = self.passwordEdit.text()

        if status == 'Rejected':
            self.deleteDetail()
            self.pendingUsers()
        elif password:
            if not is_valid_email(email) or not is_valid_password(password) or not is_valid_phone(phone):
                QMessageBox.warning(self, "Update Error", "Invalid input format")
                return

            password = self.hash_password(password)

            try:
                command = f'''
UPDATE users 
SET status = '{status}', user_type = '{type}', name = '{name}', surname = '{surname}', city = '{city}', phone = '{phone}', hashed_password = '{password}'
WHERE email = '{email}' 
'''
                cur = self.conn.cursor()
                cur.execute(command)
                cur.close()
                self.conn.commit()
                QMessageBox.information(self, "Update Successful", "Account updated successfully")

                
                self.showEditUserTab()

            except (Exception, psycopg2.DatabaseError) as error:
                QMessageBox.warning(self, "Update Error", f"{error}")

        else:
            if not is_valid_email(email) or not is_valid_phone(phone):
                QMessageBox.warning(self, "Update Error", "Invalid input format")
                return
            
            try:
                command = f'''
UPDATE users 
SET status = '{status}', user_type = '{type}', name = '{name}', surname = '{surname}', city = '{city}', phone = '{phone}'
WHERE email = '{email}' 
'''
                cur = self.conn.cursor()
                cur.execute(command)
                cur.close()
                self.conn.commit()
                QMessageBox.information(self, "Update Successful", "Account updated successfully")

                self.pendingUsers()
                self.showEditUserTab()

            except (Exception, psycopg2.DatabaseError) as error:
                QMessageBox.warning(self, "Update Error", f"{error}")


    def deleteDetail(self):
        # status = self.editUserStatus
        email = self.emailEdit.text()

        try:
            command = f'''
DELETE FROM users WHERE email = '{email}'
'''
            cur = self.conn.cursor()
            cur.execute(command)
            cur.close()
            self.conn.commit()
            QMessageBox.information(self, "Reject/Delete Successful", "Account closed successfully")

            self.pendingUsers()
            self.showEditUserTab()

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Reject/Delete Error", f"{error}")



    def selectEditUser(self, item):
        current_row = self.editUserTable.row(item)
        print(current_row)
        if current_row >= 0:
            selectedUserEmail = self.editUserTable.item(current_row, 0)
            # print(selectedUserEmail)
            if selectedUserEmail:
                print(selectedUserEmail.text())
                self.cur.execute(f"SELECT email, status, user_type, name, surname, city, phone FROM users WHERE email = '{selectedUserEmail.text()}'")
                user = self.cur.fetchone()
                print(user)
                if user:
                        email, status, user_type, name, surname, city, phone = user
                        self.emailEdit.setText(email)
                        self.nameEdit.setText(name)
                        self.surnameEdit.setText(surname)
                        self.cityEdit.setText(city)
                        self.phoneEdit.setText(phone)
                        if status == "Active":
                            self.statusCombobox.setCurrentIndex(0)
                        elif status == "Pending":
                            self.statusCombobox.setCurrentIndex(1)
                        
                        if user_type == "admin":
                            self.typeCombobox.setCurrentIndex(0)
                        elif user_type == "teacher":
                            self.typeCombobox.setCurrentIndex(1)
                        elif user_type == "student":
                            self.typeCombobox.setCurrentIndex(2)
            else:
                QMessageBox.warning(self, 'Selection Error', 'Failed to retrieve user details.')


    def changeTableStatus(self):
        self.tableStatus = self.tableStatusCombobox.currentText()
        self.loadUserForAdmin()

    def loadUserForAdmin(self):
        try:
            self.editUserTable.setRowCount(0)
            query = f"SELECT * FROM users WHERE status = '{self.tableStatus}'"
            self.cur.execute(query)
            users = self.cur.fetchall()
            for user in users:
                rowPosition = self.editUserTable.rowCount()
                self.editUserTable.insertRow(rowPosition)
                self.editUserTable.setItem(rowPosition, 0, QTableWidgetItem(str(user[1])))  
                self.editUserTable.setItem(rowPosition, 1, QTableWidgetItem(str(user[3])))  
                self.editUserTable.setItem(rowPosition, 2, QTableWidgetItem(str(user[4])))  
                self.editUserTable.setItem(rowPosition, 3, QTableWidgetItem(str(user[8])))  
                

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading users: {e}')


    def showReportsTab(self):
        self.tabWidget.setCurrentIndex(10)
        self.fromDateEdit = self.findChild(QDateEdit, "dateEdit")
        self.toDateEdit = self.findChild(QDateEdit, "dateEdit_2")
        self.fromDateEdit.setDate(datetime.date.today())
        self.toDateEdit.setDate(datetime.date.today())
        self.reportType = self.findChild(QComboBox, "comboBox")
        self.reportType.setCurrentIndex(0)
        self.selectedReportType = self.reportType.currentText()
        self.userFilter = self.findChild(QComboBox, "comboBox_2")
        self.userFilter.setCurrentIndex(0)
        self.selectedUserFilter = self.userFilter.currentText()
        self.reportTable = self.findChild(QTableWidget, 'tableWidget')
        self.generateReport = self.findChild(QPushButton, 'b6_2')

        self.reportType.currentIndexChanged.connect(self.reportTypeChange)
        self.userFilter.currentIndexChanged.connect(self.userFilterChange)
        self.userFilter.activated.connect(lambda index: self.userFilterChange(self.userFilter.itemData(index)))
        self.generateReport.clicked.connect(self.generateReportTable)

        self.populate_report_users()
        self.generateReportTable()

    def reportTypeChange(self):
        self.selectedReportType = self.reportType.currentText()

    def userFilterChange(self, user):
        if user:
            self.selectedUserFilter = user
        else: 
            self.selectedUserFilter = "All Users"

    def dateCommander(self, start_date, end_date, table=""):
        if table:
            if start_date == end_date:
                dateCommand = f"WHERE {table}.created_time >= '{start_date}' AND {table}.created_time < '{end_date}'::timestamp + INTERVAL '1 day'"
            elif start_date > end_date:
                # QMessageBox.information("Error", "Start date should be earlier than End date!")
                dateCommand = ""
            else:
                dateCommand = f''' WHERE {table}.created_time >= '{start_date}' AND {table}.created_time <= '{end_date}' '''

        else:
            if start_date == end_date:
                dateCommand = f"WHERE created_time >= '{start_date}' AND created_time < '{end_date}'::timestamp + INTERVAL '1 day'"
            elif start_date > end_date:
                # QMessageBox.information("Error", "Start date should be earlier than End date!")
                dateCommand = ''
            else:
                dateCommand = f''' WHERE created_time >= '{start_date}' AND created_time <= '{end_date}' '''
            

        return dateCommand


    def generateReportTable(self):
        start_date = self.fromDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.toDateEdit.date().toString("yyyy-MM-dd")



        if start_date > end_date:
            print("hata")
            # QMessageBox.information("Error", "Start date should be earlier than End date!")
            return

        if self.selectedUserFilter == "All Users":
            userFilterCommand = f""
        else:
            userFilterCommand = f''' AND users.email = '{self.selectedUserFilter}' '''

        if start_date == end_date:
            dateCommand = f"WHERE created_time >= '{start_date}' AND created_time < '{end_date}'::timestamp + INTERVAL '1 day'"
        elif start_date > end_date:
            # QMessageBox.information("Error", "Start date should be earlier than End date!")
            dateCommand = ""
        else:
            dateCommand = f''' WHERE created_time >= '{start_date}' AND created_time <= '{end_date}' '''


        if self.selectedReportType == 'User Actions':
            command = f'''SELECT name, surname, phone, city, email, created_time FROM users {self.dateCommander(start_date, end_date)} {userFilterCommand} ORDER BY created_time ASC'''
            column_names = ["name", "surname", "phone", "city", "email", "created_time"] 
        elif self.selectedReportType == 'Lesson Actions':
            command = f'''
SELECT lesson_name, lesson_date, lesson_time_slot, lesson_instructor, users.email  FROM lesson
inner join users
on lesson.created_by = users.user_id
{self.dateCommander(start_date, end_date, 'lesson')} 
ORDER BY lesson.created_time ASC''' 
            column_names = ["lesson_name", "lesson_date", "Time", "Instructor", "created_by"]

            pass
        elif self.selectedReportType == 'Lesson Attendance Actions':
            
            command = f'''
SELECT u.email AS user_email, l.lesson_name, la.status, ua.email AS created_by_email
FROM lessonattendance la
JOIN users ua ON la.created_by = ua.user_id
JOIN users u ON la.user_id = u.user_id
JOIN lesson l ON la.lesson_id = l.lesson_id
{self.dateCommander(start_date, end_date, "la")}
{userFilterCommand}
ORDER BY la.created_time ASC''' 
            column_names = ["Student", "Lesson", "Status", "created_by"]
            pass
        elif self.selectedReportType == 'Meeting Actions':
            command = f'''
SELECT meeting_name, meeting_date, meeting_time_slot, users.email  FROM meeting
inner join users
on meeting.created_by = users.user_id
{self.dateCommander(start_date, end_date, 'meeting')}
{userFilterCommand} 
ORDER BY meeting.created_time ASC''' 
            
            column_names = ["Meeting Name", "Date", "Time", "created_by"]
            pass
        elif self.selectedReportType == 'Meeting Attendance Actions':
            command = f'''
SELECT m.meeting_name, u.email AS user_email, ma.status, ua.email AS created_by_email 
FROM meetingattendance ma
JOIN users ua ON ma.created_by = ua.user_id
JOIN users u ON ma.user_id = u.user_id
JOIN meeting m ON ma.meeting_id = m.meeting_id
{self.dateCommander(start_date, end_date, "ma")}
{userFilterCommand}
ORDER BY ma.created_time ASC'''
            column_names = [ "Meeting", "Student", "Status", "created_by"] 
            pass
        elif self.selectedReportType == 'Announcement Actions':
            command = f'''SELECT title, message, deadline, users.email FROM announcement 
JOIN users ON announcement.created_by = users.user_id
{self.dateCommander(start_date, end_date, "announcement")}
{userFilterCommand} 
ORDER BY announcement.created_time ASC''' 
            column_names = ["Title", "Message", "Deadline", "created_by"]
            pass
        elif self.selectedReportType == 'ToDo Actions':
            command = f'''
SELECT todolist.task, todolist.task_status, todolist.deadline,  ua.email as assigned, u.email as creater FROM todolist
inner join users ua ON todolist.assigned_user_id = ua.user_id
join users u on todolist.created_by = u.user_id
{self.dateCommander(start_date, end_date, 'todolist')} 
{userFilterCommand} 
ORDER BY todolist.created_time ASC;''' 
            pass
            
            column_names = ["Task", "Task Status", "Deadline", "User", "created_by"]

        try:
            # print(command)
            self.cur.execute(command)
            self.showReport(column_names, self.cur.fetchall())
        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Report Error", str(error))

    def populate_report_users(self):
        self.cur.execute('''
SELECT user_id, name, surname, email FROM users WHERE status = 'Active'
''')
        users = self.cur.fetchall()
        for user_id, name, surname, email in users:
            display_text = f"{name} - {email}"
            self.userFilter.addItem(display_text, email)

    def showReport(self, column_names, data):
        num_columns = len(column_names)
        num_rows = len(data)

        # Set column count and headers
        self.reportTable.setColumnCount(num_columns)
        self.reportTable.setHorizontalHeaderLabels(column_names)
        header = self.reportTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Set column widths
        character_width = 30
        for i in range(num_columns):
            self.reportTable.setColumnWidth(i, len(column_names[i]) * character_width)

        # Populate the table with data
        self.reportTable.setRowCount(num_rows)
        for i in range(num_rows):
            for j in range(num_columns):
                item = QTableWidgetItem(str(data[i][j]))
                self.reportTable.setItem(i, j, item)
        
        

    





    def add_message_tab(self):
        try:
            self.sendMessage.clicked.disconnect()
        except:
            pass
        self.tabWidget.setCurrentIndex(9)
        self.message_app = MessageApp(self)    


    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)
        
#################################################################################


    def add_announce_tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.edittedAnnouncement = None
        self.populateAnnouncementCombobox()
        self.announcementCombobox_a = self.findChild(QComboBox, 'announcementCombobox_a')
        self.load_announcement()
        self.date_input = self.findChild(QLineEdit, 'announcementDate_a')

        try:
            self.addButton_a.clicked.disconnect()
            self.editButton_a.clicked.disconnect()
            self.deleteButton_a.clicked.disconnect()
        except:
            pass

        self.date_input.mousePressEvent = self.showCalendarAnnouncement
        self.addButton_a.clicked.connect(self.add_announcement)
        self.editButton_a.clicked.connect(self.edit_announcement)
        self.deleteButton_a.clicked.connect(self.delete_announcement)

        self.announcementCombobox_a.setCurrentIndex(0)
        self.announcementCombobox_a.activated.connect(lambda index: self.selectAnnouncement(self.announcementCombobox_a.itemData(index)))


    def showCalendarAnnouncement(self, event):
        calendar_pos = self.date_input.mapToGlobal(self.date_input.rect().bottomLeft())
        self.calendar.move(calendar_pos)
        self.calendar.show()

    def load_announcement(self):
        self.model = QStandardItemModel()
        self.announcementListView_a.setModel(self.model)

        self.cur.execute('''
SELECT message, deadline, created_by, title, users.email 
FROM announcement JOIN users ON created_by = users.user_id
''')
        announcements = self.cur.fetchall()
        for message, deadline, created_by, title, author in announcements:
            display_text = f'''
Author: {author}
Title: {title}
Message: {message}
Deadline: {deadline}
'''
            item = QStandardItem(display_text)
            self.model.appendRow(item)

    def selectAnnouncement(self, id):
        if not id:
            id = 0
        self.edittedAnnouncement = id
        text = self.announcementCombobox_a.currentText()
        if text != 'Select Announcement for Edit':
            self.announcementTitle_a.setText(text)
        

        self.cur.execute(f'''
SELECT message, deadline FROM announcement
WHERE announcement_id = {id} 
''')
        self.textEdit_a.clear()
        data = self.cur.fetchone()
        if data:
            context = data[0]
            self.textEdit_a.append(context)
            self.date_input.setText(str(data[1]))


    def add_announcement(self):
        text = self.textEdit_a.toPlainText()
        title = self.announcementTitle_a.text()
        date = self.date_input.text().strip()

        try:

            self.cur.execute(f'''
    INSERT INTO announcement (
    message, deadline, created_by, title
    ) VALUES (
    '{text}', '{date}', {self.user.id}, '{title}'
    );''')
            QMessageBox.warning(self, 'Success', 'Announcement Added Successfully')
            self.load_announcement()
            self.populateAnnouncementCombobox()
            self.textEdit_a.clear()
            self.announcementTitle_a.clear()
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Insert Error', f'Error: {e}')

    def edit_announcement(self):
        text = self.textEdit_a.toPlainText()
        title = self.announcementTitle_a.text()
        date = self.date_input.text().strip()

        if self.edittedAnnouncement:
            if self.edittedAnnouncement != 0:
                print(self.edittedAnnouncement)
                try:
                    self.cur.execute(f'''
            UPDATE announcement 
            SET message = '{text}', deadline = '{date}', title = '{title}'
            WHERE announcement_id = {self.edittedAnnouncement};''')
                    QMessageBox.warning(self, 'Success', 'Announcement Updated Successfully')
                    self.load_announcement()
                    self.populateAnnouncementCombobox()
                    self.textEdit_a.clear()
                    self.announcementTitle_a.clear()
                except psycopg2.Error as e:
                    QMessageBox.critical(self, 'Edit Error', f'Error: {e}')

    def delete_announcement(self):
        if self.edittedAnnouncement and self.edittedAnnouncement != 0:
            reply = QMessageBox.question(self, 'Confirm Delete', 'Are you sure you want to delete announcement?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.cur.execute(f'''
DELETE FROM announcement WHERE announcement_id = {self.edittedAnnouncement}            
''')
                    QMessageBox.warning(self, 'Success', 'Announcement Deleted Successfully')
                    self.load_announcement()
                    self.populateAnnouncementCombobox()
                    self.textEdit_a.clear()
                    self.announcementTitle_a.clear()
                except psycopg2.Error as e:
                    QMessageBox.critical(self, 'Edit Error', f'Error: {e}')
        else:
            QMessageBox.warning(self, 'Error', 'There is no selected announcement')




        
        

    def populateAnnouncementCombobox(self):
        self.announcementCombobox_a.clear()
        self.announcementCombobox_a.addItem('Select Announcement for Edit', 0)
#         
        self.cur.execute('''
SELECT title, announcement_id FROM announcement
''')
        announcement_titles = self.cur.fetchall()
        for title, announcement_id in announcement_titles:
            text = f'''{title}'''
            self.announcementCombobox_a.addItem(text, announcement_id)

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)

    def updateTeacherDetails(self):
        self.user.name = self.tb23.text()
        self.user.surname = self.tb24.text()
        self.user.phone = self.tb26.text()

        command = '''
UPDATE users
SET name = %s, surname = %s, phone = %s
WHERE users.email = %s;
'''

        try:
            cur = self.conn.cursor()
            cur.execute(command, (self.user.name, self.user.surname, self.user.phone, self.user.email))
            cur.close()
            self.conn.commit()
            QMessageBox.information(self, "Update Information", "User updated successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Update Error", str(error))   
