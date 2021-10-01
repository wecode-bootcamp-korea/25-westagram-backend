import re

def validate_email(address):
    EMAIL_PATTERN = '[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+'
    users_email   = re.match(EMAIL_PATTERN, address)

    if users_email == None:
        return False
    else:
        return users_email.group()    

def validate_password(password):
    PASSWORD_PATTERN = '(?=.*[a-z])(?=.*[0-9])(?=.*[@!#$%&?*$]).+'
    users_password   = re.match(PASSWORD_PATTERN, password)
    PASSWORD_LENGTH  = 8

    if users_password == None or len(password) < PASSWORD_LENGTH:
        return False
    else:
        return users_password.group()