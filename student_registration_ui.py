# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'student_registration.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 650)
        Form.setMaximumSize(QSize(400, 650))
        font = QFont()
        font.setPointSize(13)
        Form.setFont(font)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 401, 651))
        self.widget.setStyleSheet(u"background-color:rgb(16,16,16,255);\n"
"border-radius:20px;\n"
"")
        self.tb3 = QLineEdit(self.widget)
        self.tb3.setObjectName(u"tb3")
        self.tb3.setGeometry(QRect(20, 199, 361, 41))
        font1 = QFont()
        font1.setPointSize(10)
        self.tb3.setFont(font1)
        self.tb3.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb3.setEchoMode(QLineEdit.Normal)
        self.tb3.setClearButtonEnabled(True)
        self.tb4 = QLineEdit(self.widget)
        self.tb4.setObjectName(u"tb4")
        self.tb4.setGeometry(QRect(20, 250, 361, 41))
        self.tb4.setFont(font1)
        self.tb4.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb4.setEchoMode(QLineEdit.Password)
        self.tb4.setClearButtonEnabled(True)
        self.b3 = QPushButton(self.widget)
        self.b3.setObjectName(u"b3")
        self.b3.setGeometry(QRect(150, 510, 231, 51))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.b3.setFont(font2)
        self.b3.setStyleSheet(u"QPushButton#b3 {\n"
"    background-color: rgb(255, 191, 16);\n"
"    color: rgb(135, 60, 0);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#b3:pressed {\n"
"    background-color: rgb(255, 255, 16);\n"
"}\n"
"")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(160, 70, 81, 101))
        font3 = QFont()
        font3.setPointSize(59)
        self.label.setFont(font3)
        self.label.setStyleSheet(u"color: rgb(255, 191, 16);")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 580, 141, 21))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.label_2.setFont(font4)
        self.label_2.setStyleSheet(u"color:rgb(255,191,16);")
        self.b4 = QPushButton(self.widget)
        self.b4.setObjectName(u"b4")
        self.b4.setGeometry(QRect(260, 570, 121, 41))
        self.b4.setFont(font4)
        self.b4.setStyleSheet(u"QPushButton#b4 {\n"
"    background-color: rgb(255, 191, 16);\n"
"    color: rgb(135, 60, 0);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#b4:pressed {\n"
"    background-color: rgb(255, 255, 16);\n"
"}\n"
"")
        self.tb5 = QLineEdit(self.widget)
        self.tb5.setObjectName(u"tb5")
        self.tb5.setGeometry(QRect(20, 300, 361, 41))
        self.tb5.setFont(font1)
        self.tb5.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb5.setEchoMode(QLineEdit.Normal)
        self.tb5.setClearButtonEnabled(True)
        self.tb6 = QLineEdit(self.widget)
        self.tb6.setObjectName(u"tb6")
        self.tb6.setGeometry(QRect(20, 350, 361, 41))
        self.tb6.setFont(font1)
        self.tb6.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb6.setEchoMode(QLineEdit.Normal)
        self.tb6.setClearButtonEnabled(True)
        self.tb8 = QLineEdit(self.widget)
        self.tb8.setObjectName(u"tb8")
        self.tb8.setGeometry(QRect(20, 450, 361, 41))
        self.tb8.setFont(font1)
        self.tb8.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb8.setEchoMode(QLineEdit.Normal)
        self.tb8.setClearButtonEnabled(True)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(120, 0, 171, 51))
        font5 = QFont()
        font5.setPointSize(15)
        font5.setBold(True)
        font5.setStrikeOut(False)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"color: rgb(253, 189, 16);")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(70, 40, 251, 20))
        font6 = QFont()
        font6.setPointSize(11)
        self.label_4.setFont(font6)
        self.label_4.setStyleSheet(u"color: rgb(255, 191, 16);")
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 170, 131, 21))
        self.label_6.setFont(font4)
        self.label_6.setStyleSheet(u"color:rgb(255,191,16);")
        self.tb7 = QLineEdit(self.widget)
        self.tb7.setObjectName(u"tb7")
        self.tb7.setGeometry(QRect(20, 400, 361, 41))
        self.tb7.setFont(font1)
        self.tb7.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb7.setEchoMode(QLineEdit.Normal)
        self.tb7.setClearButtonEnabled(True)
        self.label.raise_()
        self.tb3.raise_()
        self.tb4.raise_()
        self.b3.raise_()
        self.label_2.raise_()
        self.b4.raise_()
        self.tb5.raise_()
        self.tb6.raise_()
        self.tb8.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.tb7.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tb3.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your email", None))
        self.tb4.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your password", None))
        self.b3.setText(QCoreApplication.translate("Form", u"R e g i s t e r  a s  S t u d e n t", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ue77b", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Already Registered >", None))
        self.b4.setText(QCoreApplication.translate("Form", u"L o g i n  Now", None))
        self.tb5.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Name", None))
        self.tb6.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your Surname", None))
        self.tb8.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your phone number together with '+ Country Code'", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"SMART SCHOOL", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"School-Learning-Enhancement-System", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Fill your details", None))
        self.tb7.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your City", None))
    # retranslateUi

