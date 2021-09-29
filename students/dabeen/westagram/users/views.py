# built-in module
import json
from os import access
import bcrypt
import re

# 외부 모듈
import jwt
from django.http import JsonResponse
from django.views import View

# 커스텀 모듈
from westagram.settings import ALGORITHM, SECRET_KEY
from users.models import User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=404)

            REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message': 'INVAILD_EMAIL'})

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})

            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name=data["name"],
                email=email,
                password=decoded_password,
                phone=data["phone"],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'UNKNOWN_USERS'}, status=401)

            user = User.objects.get(email=email)

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) == True:
                access_token = jwt.encode(
                    {'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)

                return JsonResponse({"access_token": access_token.decode('utf-8')}, status=200)

            return JsonResponse({'message': "INVAILD_USERS"}, status=401)

        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)

        except Exception as e:
            return JsonResponse({'message': f'{e}'})
