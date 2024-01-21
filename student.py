from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import psycopg2
from PyQt5 import QtGui
import hashlib
from validator import *
import re
import datetime
import sys
import traceback

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

    def setupUi(self):
        try:
            loadUi('student.ui', self)
        except Exception as e:
            self.showErrorMessage("Initialization Error", f"Error during StudentApp initialization: {e}")
        
        # Menu actions
        self.menu11.triggered.connect(self.edit_profile_tab)
        self.menu21_2.triggered.connect(self.view_lesson_schedule)
        self.menu22_2.triggered.connect(self.view_lesson_attendance)
        self.menu31_2.triggered.connect(self.view_meeting_schedule)
        self.menu32.triggered.connect(self.view_meeting_attendance)
        self.menu71.triggered.connect(self.logout)



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
