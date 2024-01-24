from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
import hashlib
import psycopg2
from validator import *

class RegisterApp2(QDialog):
    login = pyqtSignal(bool)

    def __init__(self, conn):
        super(RegisterApp2, self).__init__()
        loadUi("teacher_registration.ui", self)
        self.b3.clicked.connect(self.register)
        self.b4.clicked.connect(self.show_login)
        self.conn = conn

    def register(self):
        email = self.tb3.text()
        password = self.tb4.text()
        name = self.tb5.text()
        surname = self.tb6.text()
        city = self.tb7.text()
        phone = self.tb8.text()

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
            cur.execute(command, (email, password, name, surname, phone, city, 'teacher', 'Pending'))

            cur.close()

            self.conn.commit()

            QMessageBox.information(self, "Registration Successful", "Your teacher account is pending for approval")

            self.show_login()

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Registration Error", f"{error}")
 
    def show_login(self):
        self.login.emit(True)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
