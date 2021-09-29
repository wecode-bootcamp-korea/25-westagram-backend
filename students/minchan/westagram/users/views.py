import json
import re
import bcrypt
import jwt
from django.http.response   import JsonResponse
from django.views           import View
from users.models           import Users
from django.http            import HttpResponse
from my_settings            import JWT_KEY, JWT_ALGORITHM
from users.validation       import ValidationCheck
class UserRegister(View) :
    def post(self,request) :
        data            = json.loads(request.body)
        email           = data["email"]
        password        = data["password"]
        password_bcrypt = bcrypt.hashpw(bytes(password,"utf-8"),bcrypt.gensalt())

        #이메일, 패스워드의 유효성 및 중복에 대해 검사.        
        if not (email or password) :
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=401)

        if not ValidationCheck.is_email_valid(email) :
            return JsonResponse({"MESSAGE" : "이메일 양식이 틀렸습니다."}, status=401)

        if not ValidationCheck.is_pw_valid(password) :
            return JsonResponse({"MESSAGE" : "PW_regular_ERROR"}, status=401)
        
        if ValidationCheck.is_user_exist(email) :
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
    def make_jwt(self,email) :
        user_id = Users.objects.get(email=email).id
        return jwt.encode({"user_id": user_id}, JWT_KEY, algorithm=JWT_ALGORITHM)
    
    def post(self,request) :
        data        = json.loads(request.body)
        email       = data["email"]
        password    = data["password"]
        jwt_token   = self.make_jwt(email)

        if not (email and password) :
            return JsonResponse({"message": "KEY_ERROR"}, status=401)
        
        if not (ValidationCheck.is_user_exist(email) and ValidationCheck.is_pw_match(email,password)):
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        
        return JsonResponse({
            "MESSAGE": "SUCCESS",
            "access_token": jwt_token
            }, status=200
        )