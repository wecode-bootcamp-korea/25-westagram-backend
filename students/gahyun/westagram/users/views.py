import json, re

from django.http            import JsonResponse
from django.views           import View

from users.models           import User
class SignUp(View):
    def post(self, request):
        data          = json.loads(request.body)
        REGX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGX_PASSWORD = '^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$'

        try: 
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'THIS_EMAIL_ALREADY_SIGNUP'}, status=400)
            
            if not re.match(REGX_EMAIL, data['email']):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL_FORM'}, status=400)

            if not re.match(REGX_PASSWORD, data['password']):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD_FORM'}, status=400)

            User.objects.create(
                name           = data['name'],
                email          = data['email'],
                password       = data['password'],
                phone_number   = data['phone_number'],
                hobby          = data['hobby']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

            password = User.objects.get(email=data['email']).password
            if not password == data['password']:
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)