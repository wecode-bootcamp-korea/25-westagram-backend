import json
import jwt
import re
import bcrypt

from django.http     import JsonResponse
from django.views    import View

from users.models    import User
from my_settings     import SECRET_KEY, ALGORITHM

REGEX_EMAIL    = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

class SignUpView(View):

    def post(self,request):
        data = json.loads(request.body)

        encode_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        decode_password = encode_password.decode('utf-8')

        try:
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "Please use a different email"}, status=400)
            
            if not re.match(REGEX_EMAIL, data["email"]):
                return JsonResponse({"message": "Email_Error : Need @ and ."}, status=400)
            if not re.match(REGEX_PASSWORD, data["password"]):
                return JsonResponse({"message": "Password_Error : Need 8LETTER,NUMBER,SPECIAL_SYMBOLS"}, status=400)

            User.objects.create(
                name          = data['name'],
                email         = data['email'],
                password      = decode_password,
                phone_number  = data['phone_number'],
                information   = data['imformation'],
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KeyError"}, status=400)

class LoginView(View):
    def post(self,request):
        data  = json.loads(request.body)

        try :
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            users = User.objects.get(email=data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), users.password.encode('utf-8')) == True:

                access_token = jwt.encode({'id':users.id}, SECRET_KEY, algorithm=ALGORITHM)

                return JsonResponse({'token': access_token}, status=200)
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)