import json
import re

from django.views import View
from django.http  import JsonResponse
from users.models import User

class SignupView(View) :
    def post(self, request) :
        data = json.loads(request.body)

        try :
            email     = data['email']
            password  = data['password']
            birthday  = data.get('birthday', None)
            
            if not re.match('^[\w+-\_.]+@[\w]+\.[\w]+$', email) :
                return JsonResponse({'message':'이메일은 @ 와 . 이 형식에 맞게 순서대로 들어가야 합니다.'}, status=400)

            if User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'기존재 이메일입니다.'}, status=400)

            if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$', password) :
                return JsonResponse({'message':'비밀번호에는 숫자/문자/특수문자가 1개씩 들어가야 합니다.'}, status=400)

            User.objects.create(
                email     = email,
                password  = password,
                name      = data['name'],
                telephone = data['telephone'],
                birthday  = birthday
            )

            return JsonResponse({'mesage':'SUCCESS'},status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LoginView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
        
            if not User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'INVALID_USER BY EMAIL'}, status=401)
            
            if not User.objects.filter(password=password).exists() :
                return JsonResponse({'message':'INVALID USER BY PASSWORD'}, status=401)
            
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)