class User:
    def __init__(self, id, email, hashed_password, name, surname, phone, city, user_type, status, created_at):
        self.id = id
        self.email = email
        self.password = hashed_password
        self.name = name
        self.surname = surname
        self.user_type = user_type
        self.status = status
        self.created_at = created_at
        self.phone = phone
        self.city = city