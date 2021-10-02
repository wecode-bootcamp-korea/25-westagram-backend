import re
import jwt
import json
import bcrypt

from django.db.models.fields import EmailField

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name        = data['name']
            email       = data['email']
            password    = data['password']
            mobile      = data['mobile_num']
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'ALREADY_EXISTS'}, status = 400)

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '\S{8,25}'

            if not re.match(regex_email, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
            if len(data['password']) or not re.match(regex_password, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            password        = data['passdword'].encode('utf-8')
            password_crypt  = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            User.objects.create(name        =   name,
                                email       =   email, 
                                password    =   password_crypt,
                                mobile_num  =   mobile
                                )
            return JsonResponse({'message' : 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
