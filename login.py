from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from user import *
import hashlib
import os


class LoginApp(QDialog):
    authentication = pyqtSignal(object)
    student_registration = pyqtSignal(bool)
    teacher_registration = pyqtSignal(bool)

    def __init__(self, conn):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, 'login_form.ui')
        print(ui_path)
        super(LoginApp, self).__init__()
        loadUi(ui_path, self)
        self.b1.clicked.connect(self.login)
        self.b2.clicked.connect(self.show_reg)
        self.b2_2.clicked.connect(self.show_reg2)

        self.tb2.returnPressed.connect(self.login)
        self.conn = conn

    def login(self):
        email = self.tb1.text()
        password = self.tb2.text()

        cur = self.conn.cursor()

        command = '''
SELECT * FROM users 
WHERE email = %s
'''
        cur.execute(command, (email,))

        row = cur.fetchone()
        if row:
            status = row[8]

            if status == 'Pending':
                QMessageBox.warning(self, "Login Error", "Your account is pending approval.")
                return

            if self.verify_password(password, row[2]):
                user = User(*row)
                self.authentication.emit(user)
            else:
                QMessageBox.warning(self, "Login Error", "Incorrect Password")    
        else:
            QMessageBox.warning(self, "Login Error", "There is no user matched")

        cur.close()
        self.conn.commit()

    def verify_password(self, entered_password, hashed_password):
        return self.hash_password(entered_password) == hashed_password

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_reg(self):
        self.student_registration.emit(True)
        
    def show_reg2(self):
        self.teacher_registration.emit(True)
