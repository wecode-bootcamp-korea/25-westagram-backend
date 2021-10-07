import json, re
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View

from users.models           import User
from my_settings            import SECRET_KEY, ALGORITHM
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

            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name           = data['name'],
                email          = data['email'],
                password       = password,
                phone_number   = data.get('phone_number'),
                hobby          = data.get('hobby')
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(email=data['email'])

        try:
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

            password = user.password.encode('utf-8')
            
            if not bcrypt.checkpw(data['password'].encode('utf-8'), password):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)
            
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'MESSAGE': 'SUCCESS', 'access_token': access_token}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)