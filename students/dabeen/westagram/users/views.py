from django.shortcuts import render

import json
import bcrypt
import re
import jwt
from django.http import JsonResponse
from django.views import View
from users.models import User

# Create your views here.


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            # Return 400 error when using an existing email.
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'

            # Return message if not satisfied with the validation rules.
            if not re.match(regex_email, email):
                return JsonResponse({'message': 'INVAILD_EMAIL'})

            if not re.match(regex_password, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})

            # Store user's password by hash-encrypted.
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
            # Return 400 error if email or password is not delivered.
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class SignInView(View):
    def get(self, request):

        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) == True:
                    access_token = jwt.encode(
                        {'id': user.id}, 'secret', algorithm='HS256')

                    return JsonResponse(jwt.decode(access_token, 'secret', algorithm='HS256'), status=200)

                # If user enter the wrong password return 401 ERROR
                return JsonResponse({'message': 'INVAILD_USERS'}, status=401)

            # If user enter the wrong email return 401 ERROR
            return JsonResponse({'message': "INVAILD_USERS"}, status=401)
        except:
            # If user's email or password is not delivered return 400 ERROR
            return JsonResponse({'message': "KEY_ERROR"}, status=400)
