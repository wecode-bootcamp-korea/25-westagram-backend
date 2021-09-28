import json
import re
import bcrypt
from django.http.response   import JsonResponse
from django.views           import View
from users.models           import Users
from django.http            import HttpResponse
class UserRegister(View) :
    REGEX_EMAIL     = re.compile("[@][a-zA-Z]*[.]")
    REGEX_PASSWORD  = re.compile("/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[`~!@#$%^&*(),<.>/?]).{8,}")


    def is_email_valid(self,email) :
        return True if self.REGEX_EMAIL.match(email) else False

    def is_email_duplicate(self,email) :
        return Users.objects.filter(email=email).exists()
    
    def is_pw_valid(self,pw) :
        return True if self.REGEX_PASSWORD.match(pw) else False

    def post(self,request) :
        data            = json.loads(request.body)
        email           = data["email"]
        password        = data["password"]
        password_bcrypt = bcrypt.hashpw(bytes(password,"utf-8"),bcrypt.gensalt())

        #이메일, 패스워드의 유효성 및 중복에 대해 검사.        
        if not (email or password) :
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=401)

        if not self.is_email_valid(email) :
            return JsonResponse({"MESSAGE" : "이메일 양식이 틀렸습니다."}, status=401)

        if not self.is_pw_valid(password) :
            return JsonResponse({"MESSAGE" : "PW_regular_ERROR"}, status=401)
        
        if self.is_email_duplicate(email) :
            return JsonResponse({"MESSAGE" : "Email duplicate"}, status=401)
        
        Users.objects.create(
            name            = data["name"],
            email           = email,
            password        = password_bcrypt.decode('utf-8'),
            phone_number    = data["phone_number"],
            profile_etc     = data["profile_etc"],
            )

        return JsonResponse({"MESSAGE": "CREATED"}, status=201)

class UserLogin(View) :
    def is_user_exist(self,email) :
        return Users.objects.filter(email=email).exists()
    
    def is_pw_match(self,email,password) :
        return bcrypt.checkpw(password.encode('utf-8'), Users.objects.filter(email=email)[0].password.encode('utf-8'))
    
    def post(self,request) :
        data        = json.loads(request.body)
        email       = data["email"]
        password    = data["password"]

        if not (email and password) :
            return JsonResponse({"message": "KEY_ERROR"}, status=401)
        
        if not (self.is_user_exist(email) and self.is_pw_match(email,password)):
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        return JsonResponse({"message": "SUCCESS"}, status=200)