import psycopg2
from psycopg2 import sql
import hashlib 

class Database():
    def __init__(self):
        self.db_credentials = {
            'dbname': 'SmartSchool', 
            'user': 'postgres', 
            'password': '1', 
            'host': 'localhost',
            'port': '5432'
        }

        self.necessary_tables = [
            ('users','''
user_id SERIAL PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
hashed_password VARCHAR(255) NOT NULL,
name VARCHAR(50) NOT NULL,
surname VARCHAR(50) NOT NULL,
phone VARCHAR(50),
city VARCHAR(50),
user_type VARCHAR(50) NOT NULL CHECK (user_type IN ('student', 'teacher', 'admin')),
status VARCHAR(50) NOT NULL DEFAULT 'Pending',
created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''), 
            ('lesson', '''
lesson_id SERIAL PRIMARY KEY,
lesson_name VARCHAR(255) NOT NULL,
lesson_date DATE NOT NULL,
lesson_time_slot VARCHAR(11) NOT NULL,
lesson_instructor VARCHAR(50),
created_by INTEGER NOT NULL REFERENCES users(user_id),
created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''), 
            ('meeting','''
meeting_id SERIAL PRIMARY KEY,
meeting_name VARCHAR(255) NOT NULL,
meeting_date DATE NOT NULL,
meeting_time_slot VARCHAR(11) NOT NULL,
teacher_id INTEGER NOT NULL REFERENCES users(user_id),
created_by INTEGER NOT NULL REFERENCES users(user_id),
created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''), 
            ('lessonattendance', '''
  attendance_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  lesson_id INTEGER NOT NULL REFERENCES lesson(lesson_id),
  status VARCHAR(50) NOT NULL CHECK (status IN ('present', 'absent', 'late')),
  created_by INTEGER NOT NULL REFERENCES users(user_id),
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''), 
            ('meetingattendance','''
  attendance_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(user_id),
  meeting_id INTEGER NOT NULL REFERENCES meeting(meeting_id),
  status VARCHAR(50) NOT NULL CHECK (status IN ('present', 'absent', 'late')),
  created_by INTEGER NOT NULL REFERENCES users(user_id),
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''), 
            ('announcement', '''
  announcement_id SERIAL PRIMARY KEY,
  message TEXT NOT NULL,
  deadline TIMESTAMP NOT NULL,
  created_by INTEGER NOT NULL REFERENCES users(user_id),
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''),
            ('message', '''
  message_id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  sender_id INTEGER NOT NULL REFERENCES users(user_id),
  receiver_id INTEGER NOT NULL REFERENCES users(user_id),
  created_by INTEGER NOT NULL REFERENCES users(user_id),
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
'''),
            ('todolist', '''
  todo_id SERIAL PRIMARY KEY,
  task TEXT NOT NULL,
  deadline TIMESTAMP NOT NULL,
  task_status BOOLEAN NOT NULL DEFAULT false,
  assigned_user_id INTEGER NOT NULL REFERENCES users(user_id),
  created_by INTEGER NOT NULL REFERENCES users(user_id),
  created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  student_list TEXT NOT NULL
''')

            ]

    def check_db(self):    
        self.conn = psycopg2.connect(
            dbname="postgres",
            user=self.db_credentials["user"],
            password=self.db_credentials["password"],
            host=self.db_credentials["host"],
            port=self.db_credentials["port"]
        )

        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        check_db_query = sql.SQL("SELECT 1 FROM pg_database WHERE datname = {}").format(
        sql.Literal(self.db_credentials["dbname"]))

        self.cursor.execute(check_db_query)

        database_exists = self.cursor.fetchone()

        if not database_exists:
            return False
        else:
            return True

        
    def create_database(self):
        self.conn.autocommit = True
        create_db_query = sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(self.db_credentials["dbname"])
        )
        self.cursor.execute(create_db_query)

        self.cursor.close()
        self.conn.close()
        pass

    def connect_db(self):
        self.conn = psycopg2.connect(**self.db_credentials)
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def disconnect_db(self):
        self.cursor.close()
        self.conn.close()

    def check_table(self, cursor):
        self.conn.autocommit = True
        command = '''
SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE' AND table_schema = 'public'
'''
        cursor.execute(command)
        tables = [table[0] for table in cursor.fetchall()]
        for i in self.necessary_tables:
            if i[0] not in tables:
                self.create_table(cursor, i[0], i[1])
                print(f"Table '{i[0]}' created.")

    def create_table(self, cursor, table_name, table_definition):
        self.conn.autocommit = True
        command = "CREATE TABLE {} ({})".format(table_name, table_definition)

        cursor.execute(command)

    def create_table_scratch(self, cursor):
        self.conn.autocommit = True

        for i in self.necessary_tables:
            command = "CREATE TABLE {} ({})".format(i[0], i[1])
            cursor.execute(command)
            print(f"Table '{i[0]}' created.")

    def check_admin(self, cursor):
        self.conn.autocommit = True
        command = '''
SELECT * FROM users WHERE users.email = 'admin@admin.com'
'''

        cursor.execute(command)

        data = cursor.fetchone()
        if not data:
            print('admin yok')
            command = f'''
INSERT INTO users (
email, hashed_password, name, surname, user_type
) VALUES (
'admin@admin.com', '{self.hash_password('Infotech1+')}',
'Admin', 'Admin', 'admin'
);
'''
            cursor.execute(command)

    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_teachers(self, cur):
        cur.execute("SELECT name, surname FROM users WHERE user_type = 'teacher'")
        teachers = cur.fetchall()
        return teachers


    def get_students(self,cur):
        cur.execute( "SELECT  name, surname FROM users WHERE user_type = 'student' ")
        students = cur.fetchall()
        return students        






        



    