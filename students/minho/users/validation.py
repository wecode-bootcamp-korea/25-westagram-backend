import re # 정규표현식을 사용할 때 내장모듈인 re를 import해주어야 함
from django.core.exceptions import ValidationError


def validate_email(value):
    email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_regex.match(value):
        return False


def validate_password(value):
    password_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")
    if not password_regex.match(value):
        return False