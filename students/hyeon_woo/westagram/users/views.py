import json
import re

from django.http      import JsonResponse
from django.views     import View

from users.models     import User

REGEX_EMAIL    = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

class SignUpView(View):

    def post(self,request):
        data = json.loads(request.body)
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
                password      = data['password'],
                phone_number  = data['phone_number'],
                information   = data['imformation'],
            )

            return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KeyError"}, status=400)

class LoginView(View):
    def post(self,request):
        data = json.loads(request.body)
        try :
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            users = User.objects.get(email=data['email'])

            if users.password != data['password']:
                return JsonResponse( {"message": "INVALID_USER"}, status=401)
            return JsonResponse({"message":"SUCCESS"}, status=200)

        except :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
