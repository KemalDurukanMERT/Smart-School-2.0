# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_form.ui'
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
        Form.setMinimumSize(QSize(0, 0))
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.widget.setGeometry(QRect(0, 0, 400, 641))
        self.widget.setMaximumSize(QSize(400, 650))
        self.widget.setStyleSheet(u"background-color:rgb(16,16,16,255);\n"
"border-radius:20px;\n"
"")
        self.tb1 = QLineEdit(self.widget)
        self.tb1.setObjectName(u"tb1")
        self.tb1.setGeometry(QRect(20, 270, 361, 40))
        font = QFont()
        font.setPointSize(10)
        self.tb1.setFont(font)
        self.tb1.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb1.setEchoMode(QLineEdit.Normal)
        self.tb1.setClearButtonEnabled(True)
        self.tb2 = QLineEdit(self.widget)
        self.tb2.setObjectName(u"tb2")
        self.tb2.setGeometry(QRect(20, 320, 361, 40))
        self.tb2.setFont(font)
        self.tb2.setStyleSheet(u"background-color:rgb(47,49,52,200);\n"
"color:rgb(255,255,255);\n"
"border-radius:2px;\n"
"padding-left:10px;\n"
"border:1px solid rgba(0,0,0);\n"
"border-bottom-color:rgb(46,82,102,255);\n"
"padding-bottom:3px")
        self.tb2.setEchoMode(QLineEdit.Password)
        self.tb2.setClearButtonEnabled(True)
        self.b1 = QPushButton(self.widget)
        self.b1.setObjectName(u"b1")
        self.b1.setGeometry(QRect(20, 370, 361, 41))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.b1.setFont(font1)
        self.b1.setStyleSheet(u"QPushButton#b1 {\n"
"    background-color: rgb(255, 191, 16);\n"
"    color: rgb(135, 60, 0);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#b1:pressed {\n"
"    background-color: rgb(255, 255, 16);\n"
"}\n"
"")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 110, 121, 171))
        font2 = QFont()
        font2.setPointSize(92)
        font2.setBold(True)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"color: rgb(255, 191, 16);")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(40, 450, 121, 16))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(u"color:rgb(255,191,16);")
        self.b2 = QPushButton(self.widget)
        self.b2.setObjectName(u"b2")
        self.b2.setGeometry(QRect(20, 470, 161, 51))
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        self.b2.setFont(font4)
        self.b2.setStyleSheet(u"QPushButton#b2 {\n"
"    background-color: rgb(255, 191, 16);\n"
"    color: rgb(135, 60, 0);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#b2:pressed {\n"
"    background-color: rgb(255, 255, 16);\n"
"}\n"
"")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(70, 20, 271, 51))
        font5 = QFont()
        font5.setPointSize(20)
        font5.setBold(True)
        font5.setStrikeOut(False)
        self.label_3.setFont(font5)
        self.label_3.setStyleSheet(u"color: rgb(253, 189, 16);")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 70, 331, 20))
        font6 = QFont()
        font6.setPointSize(14)
        self.label_4.setFont(font6)
        self.label_4.setStyleSheet(u"color: rgb(255, 191, 16);")
        self.b2_2 = QPushButton(self.widget)
        self.b2_2.setObjectName(u"b2_2")
        self.b2_2.setGeometry(QRect(220, 470, 161, 51))
        self.b2_2.setFont(font4)
        self.b2_2.setStyleSheet(u"QPushButton#b2_2 {\n"
"    background-color: rgb(255, 191, 16);\n"
"    color: rgb(135, 60, 0);\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#b2_2:pressed {\n"
"    background-color: rgb(255, 255, 16);\n"
"}\n"
"")
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(240, 450, 121, 16))
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"color:rgb(255,191,16);")
        self.label.raise_()
        self.tb1.raise_()
        self.tb2.raise_()
        self.b1.raise_()
        self.label_2.raise_()
        self.b2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.b2_2.raise_()
        self.label_5.raise_()

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tb1.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your email", None))
        self.tb2.setPlaceholderText(QCoreApplication.translate("Form", u"Enter your password", None))
        self.b1.setText(QCoreApplication.translate("Form", u"L o g i n", None))
        self.label.setText(QCoreApplication.translate("Form", u"\ue785", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Student Sign up !!!", None))
        self.b2.setText(QCoreApplication.translate("Form", u"Sign Up as Student", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"SMART SCHOOL 2.0", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"School-Learning-Enhancement-System", None))
        self.b2_2.setText(QCoreApplication.translate("Form", u"Sign Up as Teacher", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Teacher Sign up !!!", None))
    # retranslateUi

