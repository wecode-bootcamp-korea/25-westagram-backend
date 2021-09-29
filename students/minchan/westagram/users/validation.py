import re
import bcrypt
from users.models           import Users

class ValidationCheck:
    def is_user_exist(email) :
        return Users.objects.filter(email=email).exists()

    def is_email_valid(email) :
        REGEX_EMAIL = re.compile("[@][a-zA-Z]*[.]")
        return True if REGEX_EMAIL.search(email) else False

    def is_pw_valid(password) :
        REGEX_PASSWORD  = re.compile("^(?=.*[a-zA-Z])(?=.*\d)(?=.*[`~!@#$%^&*(),<.>/?]).{8,}")
        return True if REGEX_PASSWORD.search(password) else False

    def is_pw_match(email,password) :
        return bcrypt.checkpw(password.encode('utf-8'), Users.objects.get(email=email).password.encode('utf-8'))
