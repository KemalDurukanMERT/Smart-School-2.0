import re

def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}[\]:;<>,.?/~\\-]).{8,}$"
    return re.match(pattern, password)
    
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)