import json
import re
import bcrypt
import jwt
from django.http.response   import JsonResponse
from django.views           import View
from users.models           import Users
from django.http            import HttpResponse
from my_settings            import JWT_KEY, JWT_ALGORITHM
# Create your views here.


class user_register(View):
    def valid_email(self, email):
        email_regular = re.compile("[@][a-zA-Z]*[.]")
        if email_regular.search(email) == None:
            return False
        return True

    def is_email_duplicate(self, email):
        if Users.objects.filter(email=email):
            return True  # 중복값이 있으면 True를 반환.
        return False

    def valid_pw(self, pw):
        # 검사항목 - 0: 8자리 이상, 1:문자포함, 2:숫자포함, #:특수문자포함
        test_case           = [0, 0, 0, 0]
        alphabet_regular    = re.compile("[a-zA-Z]")
        number_regular      = re.compile("[\d]")
        # 더 많은 특수문자의 허용은 [^0-9a-zA-Z]로 대체 가능.
        symbol_regular      = re.compile("[`~!@#$%^&*(),<.>/?]")
        #0 길이검사.
        if len(pw) >= 8:
            test_case[0] = 1

        #1. 알파벳 포함 검사
        for i in pw:
            if alphabet_regular.match(i) != None:
                test_case[1] = 1
                break

        #2. 숫자 포함 검사
        for i in pw:
            if number_regular.match(i) != None:
                test_case[2] = 1
                break

        #3. 특수문자 포함 검사
        for i in pw:
            if symbol_regular.match(i) != None:
                test_case[3] = 1
                break

        return test_case

    def post(self, request):
        data                = json.loads(request.body)
        data_email          = data["email"]
        data_pw             = data["password"]
        wrong_pw_message    = ""
        # 검사항목 - 0: 8자리 이상, 1:문자포함, 2:숫자포함, #:특수문자포함
        wrong_pw_list       = ["길이가 8 이하입니다.", "영문이 포함되어있지 않습니다.",
                                "숫자가 포함되어 있지 않습니다.", "특수문자가 포함되어 있지 않습니다."]
        password_check      = self.valid_pw(data_pw)
        password_bcrypt     = bcrypt.hashpw(bytes(data_pw,"utf-8"),bcrypt.gensalt())

        #1. 이메일, 패스워드 있는지 확인하기.
        if data_email == None or data_pw == None:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=401)

        #2. 이메일 유효성 검사
        if not self.valid_email(data_email):
            return JsonResponse({"MESSAGE": "이메일 양식이 틀렸습니다."}, status=401)

        #3. 패스워드 유효성 검사
        if password_check != [1, 1, 1, 1]:
            for i in range(4):
                if password_check[i] != 1:
                    wrong_pw_message += wrong_pw_list[i]
            return JsonResponse({"MESSAGE": wrong_pw_message}, status=401)

        #4. 이메울 중복 검사
        if self.is_email_duplicate(data_email):
            return JsonResponse({"MESSAGE": "Email duplicate"}, status=401)
        
        Users.objects.create(
            name        =data["name"],
            email       =data_email,
            password    =password_bcrypt,
            phone_number=data["phone_number"],
            profile_etc =data["profile_etc"],
        )

        return JsonResponse({"MESSAGE": "CREATED"}, status=201)

    def get(self, request):
        return HttpResponse("HI")


class user_login(View):
    def check_user_exist(self, email):
        # 이메일이 존재하면 True를 반환.
        if Users.objects.filter(email=email):
            return True
        return False


    def check_pw_match(self, email, pw):
        #받은 이메일,패스워드가 일치하면 True반환.
        return bcrypt.checkpw(
            bytes(pw,"utf-8"),
            Users.objects.filter(email=email)[0].password
        )
    

    def make_jwt(self, email) :
        user_id = Users.objects.filter(email=email)[0].id
        return jwt.encode({"user_id": user_id}, JWT_KEY, algorithm=JWT_ALGORITHM)


    def check_jwt(self, access_token) :
        # deocde시에 algorithm = "" 으로 하면 작동하지 않고, algorithms =[] 형태로데이터를 넣어줬더니 작동했다.
        token_object = jwt.decode(access_token, JWT_KEY, algorithms = [JWT_ALGORITHM])
        if "user_id" in token_object:
            # 다시 decode로 얻은 user_id를 다시 jwt로 만들었을 때, 데이터가 일치하는지 확인한다.
            user_id = Users.objects.filter(id=token_object["user_id"])[0].id
            re_encode = jwt.encode({"user_id": user_id}, JWT_KEY, algorithm=JWT_ALGORITHM)
            if access_token == re_encode :
                return access_token
        return False


    def post(self, request):
        data                = json.loads(request.body)
        #1.계정, 패스워드가 있는지 여부 확인
        if (not data["email"]) and (not data["password"]):
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        data_email          = data["email"]
        data_pw             = data["password"]

        #2. 계정이 있는지 여부, 3. 패스워드가 맞는지 여부
        if (not self.check_user_exist(data_email)) and (not self.check_pw_match(data_email, data_pw)):
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        #3. 토큰 발행
        jwt_token           =  self.make_jwt(data_email)

        return JsonResponse({
            "MESSAGE": "SUCCESS",
            "access_token": jwt_token
            }, status=200
        )
    
    def get(self, request):
        if "Access-Token" in request.headers : 
            access_token = request.headers["Access-Token"]
            if self.check_jwt(access_token) : 
                return HttpResponse("You are Logined!")
        return HttpResponse("YOU ARE NOT Logined!")
