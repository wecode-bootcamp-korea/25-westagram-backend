import json
import re

from django.http        import JsonResponse
from django.views       import View

from users.models       import  User


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            name        = data['name']
            email       = data['email']
            password    = data['password']
            contact     = data.get('contact')
            other_info  = data.get('other_info')

            regex_email         =   "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            regex_password      =   "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if not re.match(regex_email, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)

            if not re.match(regex_password, password):
                return JsonResponse({'message': 'INVAILD_PASSWORD'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'EMAIL_ALREADY_EXISTS'}, status=400)

            User.objects.create(
                name        =  name,
                email       =  email,
                password    =  password,
                contact     =  contact,
                other_info  =  other_info,
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status =201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'UKNOWN_USER'}, status=400)

            user = User.objects.get(email=data['email'])

            if user.password != data['password']:
                return JsonResponse({'message': 'INVAILD_USERS'}, status=401)

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400)

            