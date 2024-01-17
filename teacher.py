from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from validator import *
import psycopg2

class TeacherApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, user):
        super(TeacherApp, self).__init__()
        loadUi('teacher.ui', self)
        self.user = user
        self.conn = conn

        self.initializeUi()

    def initializeUi(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.setupMenuActions()
        self.setupButtonActions()
        # self.setupComboBoxActions()

    def setupMenuActions(self):
        self.menu11_t.triggered.connect(self.showEditProfileTab)
        self.menu21_t.triggered.connect(self.showCourseScheduleTab)
        self.menu22_t.triggered.connect(self.showLessonAttendanceTab)
        self.menu31_t.triggered.connect(self.showMeetingScheduleTab)
        self.menu32_t_2.triggered.connect(self.showMeetingAttendanceTab)
        self.menu41_t.triggered.connect(self.add_todolist_tab)
        self.menu51_t.triggered.connect(self.add_message_tab) 
        self.announcementMenu.triggered.connect(self.add_announce_tab)
        self.menu71_t.triggered.connect(self.logout)  # Logout from teacher menu

    def setupButtonActions(self):
        self.b6.clicked.connect(self.updateTeacherDetails)  

    def showEditProfileTab(self):
        self.tabWidget.setCurrentIndex(1)

        #todo ui will update
        # self.tb21.setText(self.user.teacherId)  
        self.tb22.setText(self.user.email)  
        self.tb23.setText(self.user.name)  
        self.tb24.setText(self.user.surname)  
        # self.cb11_tch.setCurrentText(self.user.gender)  
        # self.tb25.setText(self.user.date_of_birth)  
        self.tb26.setText(self.user.phone)  
        # self.tb27.setText(self.user.password)
        

    def showCourseScheduleTab(self):
        self.tabWidget.setCurrentIndex(2)
        # self.loadCurrentCourseSchedule()

    def showLessonAttendanceTab(self):
        self.tabWidget.setCurrentIndex(3)
        # self.loadStudentListForLesson()
        # self.loadCurrentCourseSchedule()
    
    def showMeetingScheduleTab(self):
        self.tabWidget.setCurrentIndex(4)
        # self.loadCurrentMeetingSchedule()

    def showMeetingAttendanceTab(self):
        self.tabWidget.setCurrentIndex(5)
        # self.loadStudentListForMeeting()
        # self.loadCurrentMeetingSchedule()

    def add_todolist_tab(self):
        self.tabWidget.setCurrentIndex(7)
        # self.view_todolist()
    
    def add_message_tab(self):
        self.tabWidget.setCurrentIndex(8)

    def add_announce_tab(self):
        self.tabWidget.setCurrentIndex(6)
        # self.load_announcements_from_json()

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)

    def updateTeacherDetails(self):
        # teacher_id = self.tb21.text()
        # email = self.tb22.text()
        self.user.name = self.tb23.text()
        self.user.surname = self.tb24.text()
        # gender = self.cb11_tch.currentText()
        # date_of_birth = self.tb25.text()
        self.user.phone = self.tb26.text()
        # password = self.tb27.text()

        command = f'''
UPDATE users
SET name = '{self.user.name}', surname = '{self.user.surname}', phone = '{self.user.phone}'
WHERE users.email = '{self.user.email}';
'''
        try:
            cur = self.conn.cursor()
            cur.execute(command)
            cur.close()
            self.conn.commit()
            QMessageBox.information(self, "Update Information", "User updated succesfully")
        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Update Error", f"{error}")
        

        

        
    