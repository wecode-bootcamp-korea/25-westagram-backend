import re

from django.core.exceptions   import ValidationError
from django.utils.translation import gettext_lazy as _

def email_validate(email) :
    if not re.match('^[\w+-\_.]+@[\w]+\.[\w]+$', email) :
        raise ValidationError(
            _(' 입력하신 이메일 %(email)s 를 확인해주세요. 이메일은 @와 . 이 순서대로 들어가야 합니다.'),
            params={'email':email}
        )

def password_validate(password) :
    if len(password) < 8 :
        raise ValidationError(
            _(' 입력하신 비밀번호 %(password)s를 확인해주세요. 8글자 이상이어야 합니다.'),
            params={'password':password}
        )

    if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$',password) :
        raise ValidationError(
            _(' 입력하신 비밀번호 %(password)s를 확인해주세요. 숫자/문자/특수문자가 한 개씩 들어가야 합니다.'),
            params={'password':password}
        )