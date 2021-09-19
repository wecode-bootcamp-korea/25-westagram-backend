import json
import re

from django.http import JsonResponse
from django.views import View
from .models import User

class UserView(View):
    def post(self, request):

        data               = json.loads(request.body)
        password_check     = data['password']
        email_check        = data['email']

        try:
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email_check):
                return JsonResponse({'MESSAGE' : 'RETYPE_EMAIL'}, status=400)

            if not re.match('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}', password_check):
                return JsonResponse({'MESSAGE' : 'RETYPE_PASSWORD'}, status=400)

            if User.objects.filter(email=email_check).exists():
                return JsonResponse({'MESSAGE' : 'EXISTING_EMAIL'}, status=400)

            User.objects.create(
                name           = data['name'],
                email          = email_check,
                password       = password_check,
                phone_number   = data['phone_number'],
                etc_info       = data['etc_info']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):

        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        try:
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status = 401)

            user = User.objects.get(email = email)

            if user.password != password:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status = 401)
            
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)

        
        except KeyError:
            return JsonResponse({'MESSAGE': 'Key_Error'}, status = 401)