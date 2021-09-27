import json
import re
from django.http.response   import JsonResponse
from django.views           import View
from users.models           import Users
from django.http            import HttpResponse

# Create your views here.
class UserRegister(View) :
    REGEX_EMAIL     = re.compile("[@][a-zA-Z]*[.]")
    REGEX_PASSWORD  = re.compile("/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[`~!@#$%^&*(),<.>/?]).{8,}")

    def valid_email(self,email) :
        return True if self.REGEX_EMAIL.match(email) else False

    def is_email_duplicate(self,email) :
        return Users.objects.filter(email=email).exists()
    
    def valid_pw(self,pw) :
        return True if self.REGEX_PASSWORD.match(pw) else False

    def post(self,request) :
        data    = json.loads(request.body)
        email   = data["email"]
        pw      = data["password"]
        #이메일, 패스워드의 유효성 및 중복에 대해 검사.        
        if not (email or pw) :
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=401)

        if not self.valid_email(email) :
            return JsonResponse({"MESSAGE" : "이메일 양식이 틀렸습니다."}, status=401)

        if not self.valid_pw(pw) :
            return JsonResponse({"MESSAGE" : "PW_regular_ERROR"}, status=401)
        
        if self.is_email_duplicate(email) :
            return JsonResponse({"MESSAGE" : "Email duplicate"}, status=401)
        
        Users.objects.create(
            name            = data["name"],
            email           = email,
            password        = pw,
            phone_number    = data["phone_number"],
            profile_etc     = data["profile_etc"],
            )

        return JsonResponse({"MESSAGE" : "CREATED"}, status=201)
