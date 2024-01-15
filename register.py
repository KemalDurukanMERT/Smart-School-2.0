from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from user import *
import bcrypt
import re
import psycopg2

class RegisterApp(QDialog):
    login = pyqtSignal(bool)

    def __init__(self, conn):
        super(RegisterApp, self).__init__()
        loadUi("register_form.ui", self)
        self.b3.clicked.connect(self.register)
        self.b4.clicked.connect(self.show_login)
        self.conn = conn

    def register(self):
        email = self.tb3.text()
        password = self.tb4.text()
        name = self.tb5.text()
        surname = self.tb6.text()

        cur = self.conn.cursor()

        if not self.is_valid_email(email) or not self.is_valid_password(password):
            QMessageBox.warning(self, "Registration Error", "Invalid input format")
            return
        
        password = self.hash_password(password)

        try:
            command = '''
INSERT INTO users (email, hashed_password, name, surname, user_type_id)
VALUES (%s, %s, %s, %s, 3)
'''
            cur.execute(command, (email, password, name, surname))

            cur.close()

            self.conn.commit()

            QMessageBox.information(self, "Registration Successfully")

            self.show_login()

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Registration Error", error)
        
        
        
        

    def show_login(self):
        self.login.emit(True)

    def is_valid_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}[\]:;<>,.?/~\\-]).{8,}$"
        return re.match(pattern, password)
    
    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password