import re

from .models import User
from django.db.utils import IntegrityError

def validate_email(address):
    email_pattern = re.compile('[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-]+')
    users_email   = re.match(email_pattern, address)

    if users_email == None:
        return False
    else:
        return users_email.group()    

def validate_password(password):
    password_pattern = re.compile('(?=.*[a-z])(?=.*[0-9])(?=.*[@!#$%&?*$]).+')
    users_password   = re.match(password_pattern, password)

    if users_password == None or len(users_password.group()) < 8:
        return False
    else:
        return users_password.group()