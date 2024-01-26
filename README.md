
# Smart School 2.0

## Overview
Smart School 2.0 is a robust school management system crafted over a period of 10 days, employing Agile methodologies and OOP principles. This Python application features a user-friendly GUI created with PyQt5 and is backed by a PostgreSQL database. Comprehensive UML and ERD diagrams offer clear insight into the system's architecture. Aimed at enhancing educational experiences, it is an excellent opportunity to demonstrate technical proficiency, problem-solving skills, and effective teamwork in 10 days.

## Features
- Utilizes Object-Oriented Programming (OOP) for clean and maintainable code.
- Integrates with PostgreSQL to manage complex data efficiently.
- Leverages UML and ERD diagrams for a clear system design and database structure.
- Implements a sleek GUI using PyQt5 for an intuitive user experience.

## Aim and Objectives
The goal of this project is to develop a system that:
- Enhances educational processes through digital solutions.
- Demonstrates technical skills in Python, GUI development, and database management.
- Encourages the use of Agile practices and collaboration in a team setting.
- Fosters problem-solving capabilities and effective project management.

## User Roles
- **Admin:** Handles account management and oversees system operations. After logging into the application, the admin is recognized and directed to the Admin Panel. Here, the admin can create teacher accounts and make modifications to these accounts. When the admin login, admin will reach the admin page. Admin should be able to run all the functions. Admin should approve/reject new accounts requested by the teacher.
- **Teacher:** Manages course schedules, student information, and educational content. Users who logged in as teachers can access the teacher interface and perform functionalities as indicated in the diagram. When the teachers login, they will reach the Teacher Page. Every teacher has a profile page that contains their own information. Teachers can create, edit and view the annual course schedule.
- **Student:** Personal account management and access to educational resources and schedules. Students can log in or create a new account. These users can modify their own personal to-do lists. Additionally, they can access to information created by their teachers. When the students login, they will reach the Student Page. They can edit their own informations. Students can view the annual course schedule (except for the teacher of those lessons).

## Methods
- Agile methodology for flexible and iterative development.
- Object-Oriented Programming principles to create a structured and scalable application.

## Tools and Technologies
- **Python 3.10.11:** Main programming language.
- **PyQt5 Designer 5.14.1:** For designing the GUI components.
- **Trello:** For task management and Agile project tracking.
- **GitHub:** For version control and collaborative development.
- **pgAdmin 4 (7.8):** PostgreSQL database management tool.
- **[dbdiagram.io](https://dbdiagram.io/d/):** For designing and documenting the database schema.
- **[app.diagrams.net](https://app.diagrams.net/):** For creating UML diagrams.

## IDE
- **Visual Studio Code:** Recommended IDE for development with support for Python and version control.

## Project Management
- Agile methodologies ensure that the project adapts to change quickly and efficiently.
- Regular meetings and use of Trello boards for task tracking and progress updates.

## Installation and Setup
Ensure PostgreSQL is installed on your computer with the username (postgres) and password set to '1'. This allows the Smart School 2.0 application to automatically generate the necessary tables and ensures smooth operation.

### Getting Started
1. Clone the repository:
   \```
   git clone https://github.com/KemalDurukanMERT/Smart-School-2.0.git
   \```
2. Navigate to the cloned directory and run:
   \```
   python main.py
   \```
   Or execute the `smartschool.exe` if available.

## Visuals

The application includes various interfaces to facilitate the management of educational activities:

<details>
  <summary>Click to view application visuals</summary>

   ![Login Screen](visuals/image1.png)
   *Initial login screen for users to access their accounts.*

   ![Student Registration](visuals/image2.png)
   *Student registration interface for creating new student accounts.*

   ![Teacher Registration](visuals/image3.png)
   *Teacher registration interface for creating new teacher accounts.*

   ![User Management](visuals/image4.png)
   *User management interface for editing or deleting user details.*

   ![Lesson Management](visuals/image5.png)
   *Interface for adding or editing lesson details.*

   ![Attendance Details](visuals/image6.png)
   *Attendance details interface for tracking student attendance.*

   ![Meeting Management](visuals/image7.png)
   *Meeting management interface for scheduling and editing meetings.*

   ![Meeting Attendance Details](visuals/image8.png)
   *Interface for adding or editing meeting attendance details.*

   ![Announcement Management](visuals/image9.png)
   *Announcement management interface for creating and editing announcements.*

   ![Task Management](visuals/image10.png)
   *Task management interface for assigning and tracking tasks.*

   ![Report Generation](visuals/image12.png)
   *Reporting interface for generating various reports.*

   ![Profile Editing](visuals/image13.png)
   *Profile editing interface for users to update their personal information.*

   ![Lesson Schedule](visuals/image14.png)
   *View of the lesson schedule interface.*

   ![Lesson Attendance](visuals/image15.png)
   *Lesson attendance records for students.*

   ![Meeting Schedule](visuals/image16.png)
   *Meeting scheduling interface for various school activities.*

   ![Meeting Attendance](visuals/image17.png)
   *Meeting attendance records showing participation status.*

   ![To-Do List](visuals/image18.png)
   *To-Do list interface for students to manage their tasks.*

   ![Announcements](visuals/image19.png)
   *Announcements interface to broadcast important messages.*

   ![Chat Interface](visuals/image20.png)
   *Chat interface for communication between users.*

</details>

## Diagrams
The project documentation includes detailed diagrams:

![Class Diagram](visuals/class_diagram.png)
*Class diagram outlining the system architecture.*

![Use Case Diagram](visuals/use_case_diagram.png)
*Use case diagram for user interactions.*

![ERD Diagram](visuals/erd_diagram.png)
*Entity-Relationship Diagram (ERD) showing the database schema.*

## Requirements
For the best experience with Smart School 2.0, users should have:
- A solid understanding of Python.
- Familiarity with database concepts and SQL.
- Knowledge of version control, preferably with Git and GitHub.
- Experience with GUI development, particularly with PyQt5.
