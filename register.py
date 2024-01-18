from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from user import *
import hashlib
import psycopg2
from validator import *

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

        if not is_valid_email(email) or not is_valid_password(password):
            QMessageBox.warning(self, "Registration Error", "Invalid input format")
            return
        
        password = self.hash_password(password)
        print(password)

        try:
            command = '''
INSERT INTO users (email, hashed_password, name, surname, user_type_id)
VALUES (%s, %s, %s, %s, 3)
'''
            cur.execute(command, (email, password, name, surname))

            cur.close()

            self.conn.commit()

            QMessageBox.information(self, "Registration Successfully", "User created succesfully")

            self.show_login()

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Registration Error", f"{error}")
        
        
        
        

    def show_login(self):
        self.login.emit(True)
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()