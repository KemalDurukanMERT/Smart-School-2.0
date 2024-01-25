from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import psycopg2
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
import hashlib
from validator import *
import re
import datetime
import sys
import traceback
from message import *
import os


def exception_hook(exctype, value, tb):
    traceback_details = '\n'.join(traceback.format_tb(tb))
    error_msg = f"Exception type: {exctype}\n"
    error_msg += f"Exception value: {value}\n"
    error_msg += f"Traceback: {traceback_details}"
    QMessageBox.critical(None, 'Unhandled Exception', error_msg)
    sys.exit(1)

sys.excepthook = exception_hook

class StudentApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, cur, database, user):
        super(StudentApp, self).__init__()
        self.conn = conn
        self.cur = self.conn.cursor()
        self.user = user
        self.setupUi()
        self.initializeUi()
        self.menu21_2.triggered.connect(self.view_lesson_schedule)
        self.menu22_2.triggered.connect(self.view_lesson_attendance)
        self.menu31_2.triggered.connect(self.view_meeting_schedule)
        self.menu32.triggered.connect(self.view_meeting_attendance)
        self.menu61_2.triggered.connect(self.add_message_tab)
        self.menu51_s.triggered.connect(self.view_todolist)
        self.announcements_s.triggered.connect(self.view_announcement)
    def add_message_tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.message_app = MessageApp(self) 

    def setupUi(self):
        loc=os.getcwd()
        try:
            loadUi(f"{loc}\\student.ui", self)
        except Exception as e:
            self.showErrorMessage("Initialization Error", f"Error during StudentApp initialization: {e}")
        
        # Menu actions
        self.menu11.triggered.connect(self.edit_profile_tab)
        self.menu21_2.triggered.connect(self.view_lesson_schedule)
        self.menu22_2.triggered.connect(self.view_lesson_attendance)
        self.menu31_2.triggered.connect(self.view_meeting_schedule)
        self.menu32.triggered.connect(self.view_meeting_attendance)
        self.menu61_2.triggered.connect(self.add_message_tab)
        self.menu71.triggered.connect(self.logout)
        self.menu51_s.triggered.connect(self.view_todolist)
        self.announcements_s.triggered.connect(self.view_announcement)


        try:
            self.b6.clicked.disconnect()
        except:
            pass
        
        # Button actions
        self.b6.clicked.connect(self.update_student_details) 
        
        # Connect the returnPressed signal to update_student_details (when you click enter)
        self.tb27.returnPressed.connect(self.update_student_details)
        
        # Load initial data
        self.load_student_details()
        self.view_lesson_schedule()
        self.view_lesson_attendance()
        self.view_meeting_schedule()
        self.view_meeting_attendance()
        self.view_todolist()
        self.view_announcement()
        
        
       
        
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        
        
        
        
        
    def logout(self):
        self.close()
        self.show_login()

    def show_login(self):
        self.login.emit(True)

    def initializeUi(self):
        # Initialize UI elements if needed
        pass

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def edit_profile_tab(self):
        self.tabWidget.setCurrentIndex(1)
        self.load_student_details()

    def load_student_details(self):
        self.cur.execute("SELECT email, name, surname, city, phone FROM users WHERE user_id = %s", (self.user.id,))
        user = self.cur.fetchone()
        if user:
            self.tb22.setText(user[0])  # email
            self.tb23.setText(user[1])  # name
            self.tb24.setText(user[2])  # surname
            self.tb25.setText(user[3])  # city
            self.tb26.setText(user[4])  # phone

    def update_student_details(self):
        email = self.tb22.text()
        name = self.tb23.text()
        surname = self.tb24.text()
        city = self.tb25.text()
        phone = self.tb26.text()
        password = self.tb27.text()

        if not is_valid_email(email) or not is_valid_password(password) or not is_valid_phone(phone):
            QMessageBox.warning(self, "Update Error", "Invalid input format")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute("UPDATE users SET email = %s, name = %s, surname = %s, city = %s, phone = %s, hashed_password = %s WHERE user_id = %s",
                         (email, name, surname, city, phone, hashed_password, self.user.id))
        self.conn.commit()
        QMessageBox.information(self, "Update Success", "Student details updated successfully.")

    def view_lesson_schedule(self):
        self.tabWidget.setCurrentIndex(2)  # Adjust the index according to your tab order
        self.lesson_table.setRowCount(0)  # Clear the table
        # Set column widths
        character_width = 12
        self.lesson_table.setColumnWidth(0, 10 * character_width)
        self.lesson_table.setColumnWidth(1, 50 * character_width)
        self.lesson_table.setColumnWidth(2, 12 * character_width)
        self.lesson_table.setColumnWidth(3, 12 * character_width)
        self.lesson_table.setColumnWidth(4, 17 * character_width)
       
       
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

    def view_lesson_attendance(self):
        self.tabWidget.setCurrentIndex(3)  # Adjust the index according to your tab order
        self.records_list_1.clear()  # Clear the list
        self.records_list_1.setFont(QtGui.QFont("Courier New", 12))  # Set monospaced font
        try:
            query = """
            SELECT la.attendance_id, l.lesson_name, l.lesson_date, l.lesson_time_slot, la.status
            FROM lessonattendance la
            JOIN lesson l ON la.lesson_id = l.lesson_id
            WHERE la.user_id = %s ORDER BY l.lesson_date ASC
            """
            self.cur.execute(query, (self.user.id,))
            records = self.cur.fetchall()
            for attendance_id, lesson_name, lesson_date, lesson_time_slot, status in records:
                lesson_date_str = lesson_date.strftime("%Y-%m-%d") if isinstance(lesson_date, datetime.date) else lesson_date
                record_text = f"Lesson: {lesson_name:40s} Date: {lesson_date_str:10s}  Time: {lesson_time_slot:13s}  Status: {status.capitalize():10s}"
                listItem = QListWidgetItem(record_text)
                listItem.setData(Qt.UserRole, attendance_id)  # Storing attendance_id as user data
                self.records_list_1.addItem(listItem)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

    def view_meeting_schedule(self):
        self.tabWidget.setCurrentIndex(4)  # Adjust the index according to your tab order
        self.meeting_table.setRowCount(0)  # Clear the table
        # Set column widths
        character_width = 12
        self.meeting_table.setColumnWidth(0, 67 * character_width)
        self.meeting_table.setColumnWidth(1, 12 * character_width)
        self.meeting_table.setColumnWidth(2, 12 * character_width)
        
        try:
            query = "SELECT meeting_id, meeting_name, meeting_date, meeting_time_slot FROM meeting ORDER BY meeting_date ASC"
            self.cur.execute(query)
            meetings = self.cur.fetchall()
            for meeting_id, meeting_name, meeting_date, meeting_time_slot in meetings:
                rowPosition = self.meeting_table.rowCount()
                self.meeting_table.insertRow(rowPosition)
                self.meeting_table.setItem(rowPosition, 0, QTableWidgetItem(meeting_name))
                meeting_date_str = meeting_date.strftime("%Y-%m-%d") if isinstance(meeting_date, datetime.date) else meeting_date
                self.meeting_table.setItem(rowPosition, 1, QTableWidgetItem(meeting_date_str))
                self.meeting_table.setItem(rowPosition, 2, QTableWidgetItem(meeting_time_slot))
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading meetings: {e}')

    def view_meeting_attendance(self):
        self.tabWidget.setCurrentIndex(5)  # Adjust the index according to your tab order
        self.records_list_2.clear()  # Clear the list
        self.records_list_2.setFont(QtGui.QFont("Courier New", 12))  # Set monospaced font

        try:
            query = """
            SELECT ma.attendance_id, m.meeting_name, m.meeting_date, m.meeting_time_slot, ma.status
            FROM meetingattendance ma
            JOIN meeting m ON ma.meeting_id = m.meeting_id
            WHERE ma.user_id = %s ORDER BY m.meeting_date ASC
            """
            self.cur.execute(query, (self.user.id,))
            records = self.cur.fetchall()
            for attendance_id, meeting_name, meeting_date, meeting_time_slot, status in records:
                meeting_date_str = meeting_date.strftime("%Y-%m-%d") if isinstance(meeting_date, datetime.date) else meeting_date
                record_text = f"Meeting: {meeting_name:40s} Date: {meeting_date_str:10s} Time: {meeting_time_slot:13s} Status: {status.capitalize():10s}"
                listItem = QListWidgetItem(record_text)
                listItem.setData(Qt.UserRole, attendance_id)  # Storing attendance_id as user data
                self.records_list_2.addItem(listItem)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

    # def view_announcement(self):
    #     self.tabWidget.setCurrentIndex(6)  # Tabloya göre dizini ayarla
    #     self.record_table_s.setRowCount(0)  # Tabloyu temizle
    #     # Kolon genişliklerini ayarla
    #     character_width = 12
    #     self.record_table_s.setColumnWidth(0, 67 * character_width)
    #     self.record_table_s.setColumnWidth(1, 12 * character_width)
    #     self.record_table_s.setColumnWidth(2, 12 * character_width)

    #     try:
    #         query = """
    #         SELECT announcement_id, message, deadline, title, created_by
    #         FROM announcement
    #         ORDER BY deadline ASC
    #         """
    #         self.cur.execute(query)
    #         records = self.cur.fetchall()

    #         # Tabloya verileri ekleyin
    #         for row, (announcement_id, announcement, deadline, title, created_by) in enumerate(records):
    #             try:
    #                 deadline_str = deadline.strftime("%Y-%m-%d") if isinstance(deadline, datetime.date) else str(deadline)
    #             except AttributeError:
    #                 # Tarih yoksa ya da hatalı biçimdeyse, hata mesajı verebilir veya farklı bir değer atayabilirsiniz.
    #                 deadline_str = "Invalid Date"

    #             self.record_table_s.insertRow(row)
    #             self.record_table_s.setItem(row, 0, QTableWidgetItem(title))
    #             self.record_table_s.setItem(row, 1, QTableWidgetItem(announcement))
    #             self.record_table_s.setItem(row, 2, QTableWidgetItem(deadline_str))

    #     except psycopg2.Error as e:
    #         QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')




    def view_announcement(self):
        self.tabWidget.setCurrentIndex(6)  # Tabloya göre dizini ayarla
        self.title_table.setRowCount(0)  # Tabloyu temizle
        # Kolon genişliklerini ayarla
        character_width = 12
        self.title_table.setColumnWidth(0, 12 * character_width)
        self.title_table.setColumnWidth(1, 64 * character_width)
        self.title_table.setColumnWidth(2, 15 * character_width)

        try:
            query = """
            SELECT announcement_id, message, deadline, title, created_by
            FROM announcement
            ORDER BY deadline ASC
            """
            self.cur.execute(query)
            records = self.cur.fetchall()

            # Tabloya verileri ekleyin
            for row, (announcement_id, announcement, deadline, title, created_by) in enumerate(records):
                try:
                    deadline_str = deadline.strftime("%Y-%m-%d") if isinstance(deadline, datetime.date) else str(deadline)
                except AttributeError:
                    # Tarih yoksa ya da hatalı biçimdeyse, hata mesajı verebilir veya farklı bir değer atayabilirsiniz.
                    deadline_str = "Invalid Date"

                self.title_table.insertRow(row)
                self.title_table.setItem(row, 0, QTableWidgetItem(title))
                item_announcement = QTableWidgetItem(announcement)
                item_announcement.setFont(QFont("Arial", weight=QFont.Bold))
                self.title_table.setItem(row, 1, QTableWidgetItem(announcement))
                self.title_table.setItem(row, 2, QTableWidgetItem(deadline_str))
                

        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Hata', f'Bir hata oluştu: {e}')







    
    def view_todolist(self):
        self.tabWidget.setCurrentIndex(7)
        self.todoTable_s.setRowCount(0)
        character_width = 12

        user_id = self.user.id
        
        # Set column widths
        self.todoTable_s.setColumnWidth(0, 10 * character_width)
        self.todoTable_s.setColumnWidth(1, 44 * character_width)
        self.todoTable_s.setColumnWidth(2, 14 * character_width)
        self.todoTable_s.setColumnWidth(3, 12 * character_width)
        self.todoTable_s.setColumnWidth(4, 17 * character_width)
        self.todoTable_s.setColumnWidth(5, 17 * character_width)
        try:
            self.todoTable_s.setRowCount(0)
            query = "SELECT todo_id, task, deadline, task_status, assigned_user_id, created_by FROM todolist WHERE assigned_user_id = %s ORDER BY deadline ASC"
            self.cur.execute(query, (user_id,))
            tasks = self.cur.fetchall()
            for task in tasks:
                rowPosition = self.todoTable_s.rowCount()
                self.todoTable_s.insertRow(rowPosition)
                
                # Inserting items into the table in the correct column order
                self.todoTable_s.setItem(rowPosition, 3, QTableWidgetItem(str(task[0]))) 
                self.todoTable_s.setItem(rowPosition, 1, QTableWidgetItem(str(task[1])))  
                self.todoTable_s.setItem(rowPosition, 2, QTableWidgetItem(str(task[2])))  
                self.todoTable_s.setItem(rowPosition, 4, QTableWidgetItem(str(task[4]))) 
                self.todoTable_s.setItem(rowPosition, 5, QTableWidgetItem(str(task[5])))
                created_by_name = self.getCreatedName(task[5]) 
                if created_by_name is not None:
                    self.todoTable_s.setItem(rowPosition, 6, QTableWidgetItem(str(created_by_name)))
                    
                else:
                    self.todoTable_s.setItem(rowPosition, 6, QTableWidgetItem("Unknown"))
                
                
                # Adding a checkbox to the third column (index 3)
                checkbox = QCheckBox()
                checkbox.setChecked(bool(task[3]))
                checkbox.stateChanged.connect(lambda state, row=rowPosition, task_id=task[0]: self.updateTaskStatus(row, task_id, state))
                self.todoTable_s.setCellWidget(rowPosition, 0, checkbox)
                
                # Hide the todo_id column after populating the table
                self.todoTable_s.setColumnHidden(3, True) 
                self.todoTable_s.setColumnHidden(4, True)  # Hides the first column (Todo ID)
                self.todoTable_s.setColumnHidden(5, True)
        except psycopg2.Error as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading lessons: {e}')
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

    def updateTaskStatus(self, row, task_id, state):
        try:
            new_status = bool(state)
            query = "UPDATE todolist SET task_status = %s WHERE todo_id = %s"
            self.cur.execute(query, (new_status, task_id))
            self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, 'Error', f'An error occurred while updating task status: {e}')
