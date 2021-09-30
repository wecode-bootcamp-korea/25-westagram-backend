import bcrypt
import json
import jwt
import re

from django.views           import View
from django.utils           import timezone
from django.http            import JsonResponse
from users.models           import User
from django.core.exceptions import ValidationError
from my_settings            import MY_ALGORITMS, MY_SECRET_KEY
from datetime               import timedelta

class SignupView(View) :
    def post(self, request) :

        try :

            data = json.loads(request.body)

            name      = data.get('name', None)
            telephone = data.get('telephone', None)
            email     = data['email']
            password  = data['password']
            birthday  = data.get('birthday', None)

            email_reg = r"^[\w+-\_.]+@[\w]+\.[\w]+$"
            regex_email     = re.compile(email_reg)

            password_reg = r"^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$"
            regex_passowrd = re.compile(password_reg)

            if not regex_email.match(email) :
                return JsonResponse({'message':'이메일은 @와 . 이 들어가야 합니다.'}, status=400)
            
            if User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'기존재 이메일입니다.'}, status=400)

            if len(password) < 8 :
                return JsonResponse({'message':'비밀번호는 최소 8글자로 설정해주세요.'}, status=400)

            if not regex_passowrd.match(password) :
                return JsonResponse({'message':'비밀번호는 숫자/문자/특수문자로 구성되어야 합니다.'}, status=400)
                
            User(
                email     = email,
                password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                name      = name,
                telephone = telephone,
                birthday  = birthday
            ).save()
            
            return JsonResponse({'mesage':'SUCCESS'},status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({'message':'최소 1개 이상의 값을 입력해야 합니다.'})

class LoginView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
        
            if not User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'계정이 존재하지 않습니다.'}, status=401)
            
            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) :

                token = jwt.encode({'email':email, 'exp':timezone.now()+timedelta(weeks=3)}, MY_SECRET_KEY, MY_ALGORITMS)
            
                return JsonResponse({'message':'SUCCESS', 'token':token}, status=200)
            
            return JsonResponse({'message':'비밀번호를 확인해주세요'}, status=401)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({'message':'최소 1개 이상의 값을 입력해야 합니다.'})