import json
import re

from users.models import User
from django.http import JsonResponse
from django.views import View

# Create your views here.


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message': 'INVAILD_EMAIL'})

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})

            User.objects.create(
                name=data["name"],
                email=email,
                password=password,
                phone=data["phone"],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'

            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'message': 'INVAILD_EMAIL'})

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})

            User.objects.create(
                name=data["name"],
                email=email,
                password=password,
                phone=data["phone"],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)


class SignInView(View):
    # Use User's email and password
    def get(self, request):
        data = json.loads(request.body)
        try:

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if user.password == data['password']:
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                # If user enter the wrong password return 401 ERROR
                return JsonResponse({'message': 'INVAILD_USERS'}, status=401)

            # If user enter the wrong email return 401 ERROR
            return JsonResponse({'message': "INVAILD_USERS"}, status=401)

        except:
            # If user's email or password is not delivered return 400 ERROR
            return JsonResponse({'message': "KEY_ERROR"}, status=400)
