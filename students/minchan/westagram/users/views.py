import json
import re
#import bcrypt
from django.http.response   import JsonResponse
from django.views           import View
from users.models           import Users
from django.http            import HttpResponse

# Create your views here.
class user_register(View) :
    def valid_email(self,email) :
        email_regular = re.compile("[@][a-zA-Z]*[.]")
        if email_regular.search(email) == None :
            return False
        return True


    def is_email_duplicate(self,email) :
        if Users.objects.filter(email=email) :
            return True # 중복값이 있으면 True를 반환.
        return False
    

    def valid_pw(self,pw) :
        # 검사항목 - 0: 8자리 이상, 1:문자포함, 2:숫자포함, #:특수문자포함
        test_case           = [0,0,0,0]
        alphabet_regular    = re.compile("[a-zA-Z]")
        number_regular      = re.compile("[\d]")
        symbol_regular      = re.compile("[`~!@#$%^&*(),<.>/?]") #더 많은 특수문자의 허용은 [^0-9a-zA-Z]로 대체 가능.
        #0 길이검사.
        if len(pw) >= 8 : 
            test_case[0] = 1

        #1. 알파벳 포함 검사
        for i in pw :
            if alphabet_regular.match(i) != None :
                test_case[1] = 1
                break

        #2. 숫자 포함 검사
        for i in pw :
            if number_regular.match(i) != None :
                test_case[2] = 1
                break

        #3. 특수문자 포함 검사
        for i in pw :
            if symbol_regular.match(i) != None :
                test_case[3] = 1
                break

        return test_case  


    def post(self,request) :
        data                = json.loads(request.body)
        data_email          = data["email"]
        data_pw             = data["password"]
        wrong_pw_message    = ""
        # 검사항목 - 0: 8자리 이상, 1:문자포함, 2:숫자포함, #:특수문자포함
        wrong_pw_list       = ["길이가 8 이하입니다.", "영문이 포함되어있지 않습니다.", "숫자가 포함되어 있지 않습니다.", "특수문자가 포함되어 있지 않습니다."]
        password_check      = self.valid_pw(data_pw)
        
        #1. 이메일, 패스워드 있는지 확인하기.
        if data_email == None or data_pw == None :
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=401)

        #2. 이메일 유효성 검사
        if not self.valid_email(data_email) :
            return JsonResponse({"MESSAGE" : "이메일 양식이 틀렸습니다."}, status=401)
        
        #3. 패스워드 유효성 검사
        if  password_check != [1,1,1,1] :
            for i in range(4) :
                if password_check[i] != 1 :
                    wrong_pw_message += wrong_pw_list[i]
            return JsonResponse({"MESSAGE" : wrong_pw_message}, status=401)
        
        #4. 이메울 중복 검사
        if self.is_email_duplicate(data_email) :
            return JsonResponse({"MESSAGE" : "Email duplicate"}, status=401)
        
        Users.objects.create(
            name            = data["name"],
            email           = data_email,
            password        = data["pw"],
            phone_number    = data["phone_number"],
            profile_etc     = data["profile_etc"],
            )

        return JsonResponse({"MESSAGE" : "CREATED"}, status=201)

    def get(self,request) :
        return HttpResponse("HI")

class user_login(View) :
    def check_user_exist(self,email) :
        # 이메일이 존재하면 True를 반환.
        if Users.objects.filter(email=email) :
            return True
        return False
    
    def check_pw_match(self,email,pw) :
        #받은 이메일,패스워드가 일치하면 True반환.
        return Users.objects.filter(email=email)[0].password == pw


    def post(self,request) :
        data        = json.loads(request.body)
        data_email  = data["email"]
        data_pw     = data["password"]

        #1.계정, 패스워드가 있는지 여부
        if (not data_email) and (not data_pw) :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        #2. 계정이 있는지 여부, 3. 패스워드가 맞는지 여부
        if (not self.check_user_exist(data_email)) and (not self.check_pw_match(data_email,data_pw)):
            return JsonResponse({"message": "INVALID_USER"}, status=401)    

        return JsonResponse({"message": "SUCCESS"}, status=200)

