import re

from django.core.exceptions                 import ValidationError

def validate_email(value) :
    email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_regex.match(value):
        raise ValidationError('INVALID_EMAIL_ADDRESS')
        

def validate_password(value) :
    password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
    if not password_regex.match(value):
        raise ValidationError('INVALID_PASSWORD')