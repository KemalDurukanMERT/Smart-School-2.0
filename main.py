import sys
import re
from login import *
from register import *
import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication 


class SchoolSystem():
    def __init__(self):
        self.user = None
        self.connect_db({'dbname': 'SmartSchool', 'user': 'postgres', 'password': '1', 'host': 'localhost'})
        
        login_form = LoginApp(self.conn)
        register_form = RegisterApp(self.conn)

        login_form.authentication.connect(self.login_success)
        login_form.register.connect(self.show_reg)

        widget.addWidget(login_form)
        widget.addWidget(register_form)
        widget.show()
        sys.exit(app.exec_())

    def connect_db(self, credentials):
        try:
            self.conn = psycopg2.connect(**credentials)
            cur = self.conn.cursor()

            if self.conn and cur:
                print("connected to database") 

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def login_success(self, user):
        self.user = user
        print(self.user.email)

    def show_reg(self):
        global widget
        widget.setCurrentIndex(1)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    system = SchoolSystem()



#############################################################################################################
# ! DATA LOAD SAVE
#############################################################################################################

def load_users():
    pass

def save_users():
    pass

def load_lessons():
    pass

def save_lessons():
    pass

def load_lesson_attendance():
    pass

def save_lesson_attendance():
    pass

def load_meetings():
    pass

def save_meetings():
    pass

def load_meeting_attendance():
    pass

def save_meeting_attendance():
    pass

def load_announcement():
    pass

def save_announcement():
    pass

def load_todo():
    pass

def save_todo():
    pass

#############################################################################################################
# ! VALIDATION
#############################################################################################################

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}[\]:;<>,.?/~\\-]).{8,}$"
    return re.match(pattern, password)

def is_valid_phone(phone):
    return re.match(r"^\+\d{1,3}\d{9}$", phone)



