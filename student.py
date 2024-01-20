from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QComboBox, QListWidget, QHeaderView, QMessageBox, QWidget, QCalendarWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import psycopg2
import re
import datetime

class StudentApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, cur, database, user):
        super(StudentApp, self).__init__()
        self.setupUi()
        self.connectDatabase(conn, cur, database)
        self.user = user
        self.initializeUi()

    def setupUi(self):
        try:
            loadUi('student.ui', self)
        except Exception as e:
            self.showErrorMessage("Initialization Error", f"Error during StudentApp initialization: {e}")
    
    def initializeUi(self):
        pass

    def showErrorMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def connectDatabase(self, conn, cur, database):
        self.conn = conn
        self.cur = cur
        self.database = database

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)

