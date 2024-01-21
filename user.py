class User:
    def __init__(self, user_id, email, hashed_password, name, surname, phone, city, user_type, status, created_time):
        self.id = user_id
        self.email = email
        self.password = hashed_password
        self.name = name
        self.surname = surname
        self.user_type = user_type
        self.status = status
        self.created_time = created_time
        self.phone = phone
        self.city = city