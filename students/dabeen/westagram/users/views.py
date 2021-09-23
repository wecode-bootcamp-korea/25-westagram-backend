from users.models import User
from django.shortcuts import render

import json
import re
from django.http import JsonResponse
from django.views import View


class SignUpView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            email = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

            regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}'

            if not re.match(regex_email, email):
                return JsonResponse({'message': 'INVAILD_EMAIL'})

            if not re.match(regex_password, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'})

            User.objects.create(
                name=data["name"],
                email=email,
                password=password,
                phone=data["phone"],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
