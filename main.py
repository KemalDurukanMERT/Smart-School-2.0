import sys
import re
from login import *
from student_registration import *
from teacher_registration import *
import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication 
from database import *
from teacher import *
from student import *

class SchoolSystem():
    def __init__(self):
        self.database = Database()
        if self.database.check_db():
            self.conn, self.cur = self.database.connect_db()
            self.database.check_table(self.cur)
            self.database.check_admin(self.cur)
        else:
            self.database.create_database()
            self.conn, self.cur = self.database.connect_db()
            self.database.create_table_scratch(self.cur)
            self.database.check_admin(self.cur)



        self.user = None
        
        
        self.login_form = LoginApp(self.conn)
        self.student_registration = RegisterApp(self.conn)
        self.teacher_registration = RegisterApp2(self.conn)
        

        self.login_form.authentication.connect(self.login_success)
        self.login_form.student_registration.connect(self.show_reg)
        self.student_registration.login.connect(self.show_login)
        
        self.login_form.teacher_registration.connect(self.show_reg2)
        self.teacher_registration.login.connect(self.show_login)
        
        
        

        widget.addWidget(self.login_form)
        widget.addWidget(self.student_registration)
        widget.addWidget(self.teacher_registration)

        widget.show()
        widget.setFixedWidth(400)
        widget.setFixedHeight(650)
        sys.exit(app.exec_())

    def login_success(self, user):
        self.user = user
        print(self.user.email)
        print(self.user.user_type)
        
        global widget
        widget.hide()

        if self.user.user_type == "admin":
            pass
        elif self.user.user_type == "teacher":
            print('teacher')
            self.teacher_app = TeacherApp(self.conn, self.cur, self.database, self.user)
            self.teacher_app.show()
            self.teacher_app.login.connect(self.show_login)

        elif self.user.user_type == "student":
            print('student')
            self.student_app = StudentApp(self.conn, self.cur, self.database, self.user)
            self.student_app.show()
            self.student_app.login.connect(self.show_login)
        


    def show_reg(self):
        global widget
        widget.setCurrentIndex(1)
        
    def show_reg2(self):
        global widget
        widget.setCurrentIndex(2)
        
        
    def show_login(self):
        global widget
        self.login_form.tb1.clear()
        self.login_form.tb2.clear()
        widget.show()
        
        widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    system = SchoolSystem()
    widget.setFixedWidth(400)
    widget.setFixedHeight(650)
    





