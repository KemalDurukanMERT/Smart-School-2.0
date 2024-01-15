class User:
    def __init__(self, id, email, password, name, surname, user_type, status, created_at, phone="", city=""):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.surname = surname
        if user_type == 1:
            self.user_type = "admin"
        elif user_type == 2:
            self.user_type = "teacher"
        elif user_type == 3:
            self.user_type = "student"
        self.status = status
        self.created_at = created_at
        self.phone = phone
        self.city = city