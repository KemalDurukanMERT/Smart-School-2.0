import psycopg2
import hashlib

class Database:
    def __init__(self):
        self.db_credentials = {
            'dbname': 'SmartSchool',
            'user': 'postgres',
            'password': '1',
            'host': 'localhost',
            'port': '5432'
        }

    def connect_db(self):
        self.conn = psycopg2.connect(**self.db_credentials)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.cursor.close()
        self.conn.close()

    def add_sample_users(self):
        sample_users = [
            ('teacher@example.com', 'Teacher', 'Teacher', 'teacher'),
            ('student@example.com', 'Student', 'Student', 'student'),
            ('admin@example.com', 'Admin', 'Admin', 'admin')
        ]

        for email, name, surname, user_type in sample_users:
            hashed_password = self.hash_password('Infotech1+')
            insert_user_query = '''
                INSERT INTO users (email, hashed_password, name, surname, user_type)
                VALUES (%s, %s, %s, %s, %s);
            '''

            user_data = (email, hashed_password, name, surname, user_type)
            self.cursor.execute(insert_user_query, user_data)
            print(f"Sample {user_type} user added.")

        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

if __name__ == "__main__":
    # Create a Database object and connect to the database
    database = Database()
    database.connect_db()

    # Add sample users to the database
    database.add_sample_users()

    # Disconnect from the database
    database.disconnect_db()
