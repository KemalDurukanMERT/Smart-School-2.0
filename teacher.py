from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QComboBox, QHeaderView, QMessageBox, QWidget, QCalendarWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
import psycopg2
import re

class TeacherApp(QMainWindow):
    login = pyqtSignal(bool)

    def __init__(self, conn, cur, database, user):
        super(TeacherApp, self).__init__()
        self.setupUi()
        self.connectDatabase(conn, cur, database)
        self.user = user
        self.initializeUi()

    def setupUi(self):
        try:
            loadUi('teacher.ui', self)
            self.selected_lesson_index = None
            self.selected_meeting_index = None
            self.comboBox_instructor.currentIndexChanged.connect(self.onInstructorChanged)
        except Exception as e:
            self.showErrorMessage("Initialization Error", f"Error during TeacherApp initialization: {e}")

    def connectDatabase(self, conn, cur, database):
        self.conn = conn
        self.cur = cur
        self.database = database
        self.populate_instructors()

    def initializeUi(self):
        self.setupTabs()
        self.setupMenuActions()
        self.setupButtonActions()
        self.setupCalendar()
        self.setupMeetingCalendar()

    def setupTabs(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)

    def setupMenuActions(self):
        self.menu11_t.triggered.connect(self.showEditProfileTab)
        self.menu21_t.triggered.connect(self.showLessonScheduleTab)
        self.menu22_t.triggered.connect(self.showLessonAttendanceTab)
        self.menu31_t.triggered.connect(self.showMeetingScheduleTab)
        self.menu32_t_2.triggered.connect(self.showMeetingAttendanceTab)
        self.menu41_t.triggered.connect(self.add_todolist_tab)
        self.menu51_t.triggered.connect(self.add_message_tab)
        self.announcementMenu.triggered.connect(self.add_announce_tab)
        self.menu71_t.triggered.connect(self.logout)

    def setupButtonActions(self):
        self.b6.clicked.connect(self.updateTeacherDetails)

    def setupCalendar(self):
        self.calendar = QCalendarWidget(self)
        self.calendar.setWindowFlags(Qt.Popup)
        self.calendar.setGridVisible(True)
        self.calendar.hide()
        self.calendar.clicked.connect(self.updateDateInput)

    def onInstructorChanged(self, index):
        if index == 0:
            pass  # Placeholder is selected, handle this case separately if needed
        else:
            selected_instructor = self.comboBox_instructor.currentText()

    def showEditProfileTab(self):
        self.tabWidget.setCurrentIndex(1)
        self.tb22.setText(self.user.email)
        self.tb23.setText(self.user.name)
        self.tb24.setText(self.user.surname)
        self.tb26.setText(self.user.phone)

    def updateDateInput(self, date):
        formatted_date = date.toString("dd-MM-yyyy")
        self.date_input.setText(formatted_date)
        self.calendar.hide()

    def showLessonScheduleTab(self):
        self.tabWidget.setCurrentIndex(2)
        # Initialize UI elements for lesson schedule management
        self.date_input = self.findChild(QLineEdit, 'dateInput')
        self.lesson_name = self.findChild(QLineEdit, 'lessonName')
        self.time_slot = self.findChild(QLineEdit, 'timeSlot')
        self.add_lesson_btn = self.findChild(QPushButton, 'addLessonBtn')
        self.delete_lesson_btn = self.findChild(QPushButton, 'deleteLessonBtn')
        self.delete_all_lessons_btn = self.findChild(QPushButton, 'deleteAllLessonsBtn')
        self.comboBox_instructor = self.findChild(QComboBox, 'comboBox_instructor')
        self.lesson_table = self.findChild(QTableWidget, 'lessonTable')

        self.lesson_table.setColumnCount(4)
        self.lesson_table.setHorizontalHeaderLabels(["Lesson Name", "Date", "Time", "Instructor"])
        header = self.lesson_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        self.add_lesson_btn.clicked.connect(self.addLesson)
        self.date_input.mousePressEvent = self.showCalendar
        self.delete_lesson_btn.clicked.connect(self.deleteLesson)
        self.delete_all_lessons_btn.clicked.connect(self.deleteAllLessons)
        self.lesson_table.itemClicked.connect(self.selectLesson)

        # Set column widths
        character_width = 12
        self.lesson_table.setColumnWidth(0, 54 * character_width)
        self.lesson_table.setColumnWidth(1, 10 * character_width)
        self.lesson_table.setColumnWidth(2, 10 * character_width)
        self.lesson_table.setColumnWidth(3, 14 * character_width)

    def resetForm(self):
        self.lesson_name.clear()
        self.date_input.clear()
        self.time_slot.clear()
        self.comboBox_instructor.setCurrentIndex(0)

    def populate_instructors(self):
        try:
            self.comboBox_instructor.clear()
            self.comboBox_instructor.addItem("Select an instructor")
            teachers = self.database.get_teachers(self.cur)
            for name, surname in teachers:
                self.comboBox_instructor.addItem(f"{name} {surname}")
        except Exception as e:
            self.showErrorMessage("Database Error", f"Error populating instructors: {e}")

    def isValidTimeSlot(self, time_slot):
        pattern = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')
        return pattern.match(time_slot) is not None

    def showCalendar(self, event):
        calendar_pos = self.date_input.mapToGlobal(self.date_input.rect().bottomLeft())
        self.calendar.move(calendar_pos)
        self.calendar.show()

    def selectLesson(self, item):
        current_row = self.lesson_table.row(item)
        if current_row >= 0:
            lesson_item = self.lesson_table.item(current_row, 0)
            date_item = self.lesson_table.item(current_row, 1)
            time_item = self.lesson_table.item(current_row, 2)
            if lesson_item and date_item and time_item:
                lesson_name = lesson_item.text()
                date = date_item.text()
                time = time_item.text()
                self.lesson_name.setText(lesson_name)
                self.date_input.setText(date)
                self.time_slot.setText(time)
                self.selected_lesson_index = current_row
            else:
                print("Some items are None!")

    def addLesson(self):
        lesson_name = self.lesson_name.text().strip()
        date = self.date_input.text().strip()
        time = self.time_slot.text().strip()
        instructor_index = self.comboBox_instructor.currentIndex()
        instructor = self.comboBox_instructor.currentText()

        if not lesson_name or not date or not time or instructor_index == 0:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out and a valid instructor must be selected.")
            return

        if not self.isValidTimeSlot(time):
            QMessageBox.warning(self, "Input Error", "Time slot must be in the format xx:xx-xx:xx.")
            return

        if self.selected_lesson_index is not None:
            rowPosition = self.selected_lesson_index
        else:
            rowPosition = self.lesson_table.rowCount()
            self.lesson_table.insertRow(rowPosition)

        lesson_item = QTableWidgetItem(lesson_name)
        date_item = QTableWidgetItem(date)
        time_item = QTableWidgetItem(time)
        instructor_item = QTableWidgetItem(instructor)

        lesson_item.setToolTip(lesson_name)
        date_item.setTextAlignment(Qt.AlignCenter)
        time_item.setTextAlignment(Qt.AlignCenter)
        instructor_item.setTextAlignment(Qt.AlignCenter)

        self.lesson_table.setItem(rowPosition, 0, lesson_item)
        self.lesson_table.setItem(rowPosition, 1, date_item)
        self.lesson_table.setItem(rowPosition, 2, time_item)
        self.lesson_table.setItem(rowPosition, 3, instructor_item)

        self.resetForm()
        self.selected_lesson_index = None

    def deleteLesson(self):
        selected_rows = set()
        for item in self.lesson_table.selectedItems():
            selected_rows.add(item.row())
        for row in sorted(selected_rows, reverse=True):
            self.lesson_table.removeRow(row)
        
        self.resetForm()
        self.selected_lesson_index = None

    def deleteAllLessons(self):
        self.lesson_table.setRowCount(0)
        self.resetForm()
        
###########################################################################################################
    def showLessonAttendanceTab(self):
        self.tabWidget.setCurrentIndex(3)
###########################################################################################################
    
    def showMeetingScheduleTab(self):
        #try:
            self.tabWidget.setCurrentIndex(4)
            
            #Find or create UI elements for meeting schedule management
            self.meeting_date_input = self.findChild(QLineEdit, 'meetingDateInput')
            # print("Meeting Date Input:", self.meeting_date_input)  # This should not print None

            self.meeting_title = self.findChild(QLineEdit, 'meetingTitle')
            self.meeting_time_slot = self.findChild(QLineEdit, 'meetingTimeSlot')
            self.add_meeting_btn = self.findChild(QPushButton, 'addMeetingBtn')
            if self.add_meeting_btn is None:
                print("add_meeting_btn not found")
            self.delete_meeting_btn = self.findChild(QPushButton, 'deleteMeetingBtn')
            self.delete_all_meetings_btn = self.findChild(QPushButton, 'deleteAllMeetingsBtn')

            # Initialize the meeting table
            self.meeting_table = self.findChild(QTableWidget, 'meetingTable')
            self.meeting_table.setColumnCount(3)
            self.meeting_table.setHorizontalHeaderLabels(["Meeting Title", "Meeting Date", "Meeting Time"])
            
            # Set resize mode and selection behavior for the meeting table
            header = self.meeting_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            self.meeting_table.setSelectionBehavior(QTableWidget.SelectRows)
            
            # Connect buttons to their respective functions
            self.add_meeting_btn.clicked.connect(self.addMeeting)
            self.meeting_date_input.mousePressEvent = self.showMeetingCalendar  # Reuse the calendar for meeting dates
            self.delete_meeting_btn.clicked.connect(self.deleteMeeting)
            self.delete_all_meetings_btn.clicked.connect(self.deleteAllMeetings)
            self.meeting_table.itemClicked.connect(self.selectMeeting)
            
            # Set column widths (adjust character_width based on your font and font size)
            character_width = 12
            self.meeting_table.setColumnWidth(0, 35 * character_width)  # Set width for meeting title column
            self.meeting_table.setColumnWidth(1, 12 * character_width)   # Set width for date column
            self.meeting_table.setColumnWidth(2, 12 * character_width)   # Set width for time column
        # except Exception as e:
        #     print(f"Error in showMeetingScheduleTab: {e}")
        #     QMessageBox.warning(self, "Error", f"An error occurred in showMeetingScheduleTab: {str(e)}")
    
    def setupMeetingCalendar(self):
        self.meeting_calendar = QCalendarWidget(self)
        self.meeting_calendar.setWindowFlags(Qt.Popup)
        self.meeting_calendar.setGridVisible(True)
        self.meeting_calendar.hide()
        self.meeting_calendar.clicked.connect(self.updateMeetingDateInput)
    
    def updateMeetingDateInput(self, date):
        formatted_meeting_date = date.toString("dd-MM-yyyy")
        self.meeting_date_input.setText(formatted_meeting_date)
        self.meeting_calendar.hide()
    
    def isValidTimeSlot(self, time_slot):
        pattern = re.compile(r'^\d{2}:\d{2}-\d{2}:\d{2}$')
        return pattern.match(time_slot) is not None
    
    def showMeetingCalendar(self, event):
        meeting_calendar_pos = self.meeting_date_input.mapToGlobal(self.meeting_date_input.rect().bottomLeft())
        self.meeting_calendar.move(meeting_calendar_pos)
        self.meeting_calendar.show()

    def selectMeeting(self, item):
        current_row = self.meeting_table.row(item)
        if current_row >= 0:
            meeting_item = self.meeting_table.item(current_row, 0)
            date_item = self.meeting_table.item(current_row, 1)
            time_item = self.meeting_table.item(current_row, 2)
            if meeting_item and date_item and time_item:
                meeting_name = meeting_item.text()
                date = date_item.text()
                time = time_item.text()
                self.meeting_name.setText(meeting_name)
                self.date_input.setText(date)
                self.time_slot.setText(time)
                self.selected_meeting_index = current_row
            else:
                print("Some items are None!")

    def addMeeting(self):
        try:
            print("Adding meeting...")
            title = self.meeting_title.text().strip()
            date = self.meeting_date_input.text().strip()
            time = self.meeting_time_slot.text().strip()
            print(f"Title: {title}, Date: {date}, Time: {time}")

            if not title or not date or not time:
                QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
                return

            if not self.isValidTimeSlot(time):
                QMessageBox.warning(self, "Input Error", "Time slot must be in the format xx:xx-xx:xx.")
                return

            if self.selected_meeting_index is not None:
                rowPosition = self.selected_meeting_index
            else:
                rowPosition = self.meeting_table.rowCount()
                self.meeting_table.insertRow(rowPosition)

            meeting_item = QTableWidgetItem(title)
            date_item = QTableWidgetItem(date)
            time_item = QTableWidgetItem(time)

            meeting_item.setToolTip(title)  # Set tooltip to show full meeting title on hover

            self.meeting_table.setItem(rowPosition, 0, meeting_item)
            self.meeting_table.setItem(rowPosition, 1, date_item)
            self.meeting_table.setItem(rowPosition, 2, time_item)

            self.meeting_title.clear()
            self.meeting_date_input.clear()
            self.meeting_time_slot.clear()

            self.selected_meeting_index = None
            print("Meeting added successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            print(f"Error in addMeeting: {e}")



    def deleteMeeting(self):
        try:
            print("Deleting selected meeting...")
            selected_rows = set()
            for item in self.meeting_table.selectedItems():
                selected_rows.add(item.row())
            for row in sorted(selected_rows, reverse=True):
                self.meeting_table.removeRow(row)

            self.meeting_title.clear()
            self.meeting_date_input.clear()
            self.meeting_time_slot.clear()
            print("Selected meeting(s) deleted.")
        except Exception as e:
            print(f"Error in deleteMeeting: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred in deleteMeeting: {str(e)}")



    def deleteAllMeetings(self):
        try:
            print("Deleting all meetings...")
            self.meeting_table.setRowCount(0)
            self.meeting_title.clear()
            self.meeting_date_input.clear()
            self.meeting_time_slot.clear()
            print("All meetings deleted.")
        except Exception as e:
            print(f"Error in deleteAllMeetings: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred in deleteAllMeetings: {str(e)}")

    def selectMeeting(self, item):
        try:
            print("Selecting meeting...")
            current_row = self.meeting_table.row(item)
            if current_row >= 0:
                title_item = self.meeting_table.item(current_row, 0)
                date_item = self.meeting_table.item(current_row, 1)
                time_item = self.meeting_table.item(current_row, 2)

                if title_item and date_item and time_item:
                    title = title_item.text()
                    date = date_item.text()
                    time = time_item.text()

                    self.meeting_title.setText(title)
                    self.meeting_date_input.setText(date)
                    self.meeting_time_slot.setText(time)
                    self.selected_meeting_index = current_row
                    print(f"Meeting selected: Title: {title}, Date: {date}, Time: {time}")
                else:
                    print("Some items are None!")
            else:
                print("No meeting selected.")
        except Exception as e:
            print(f"Error in selectMeeting: {e}")
            QMessageBox.warning(self, "Selection Error", f"An error occurred in selectMeeting: {str(e)}")

###########################################################################################################
    def showMeetingAttendanceTab(self):
        self.tabWidget.setCurrentIndex(5)
###########################################################################################################
    def add_todolist_tab(self):
        self.tabWidget.setCurrentIndex(7)

    def add_message_tab(self):
        self.tabWidget.setCurrentIndex(8)

    def add_announce_tab(self):
        self.tabWidget.setCurrentIndex(6)

    def logout(self):
        self.close()
        self.show_login()
    
    def show_login(self):
        self.login.emit(True)

    def updateTeacherDetails(self):
        self.user.name = self.tb23.text()
        self.user.surname = self.tb24.text()
        self.user.phone = self.tb26.text()

        command = '''
UPDATE users
SET name = %s, surname = %s, phone = %s
WHERE users.email = %s;
'''

        try:
            cur = self.conn.cursor()
            cur.execute(command, (self.user.name, self.user.surname, self.user.phone, self.user.email))
            cur.close()
            self.conn.commit()
            QMessageBox.information(self, "Update Information", "User updated successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.warning(self, "Update Error", str(error))
