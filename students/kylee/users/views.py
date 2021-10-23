import bcrypt
import json
import jwt
import re

from django.views           import View
from django.utils           import timezone
from django.http            import JsonResponse
from users.models           import User
from westagram.settings     import ALGORITHMS ,SECRET_KEY
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

            PASSWORD_LENGTH = 8

            email_reg   = r"^[\w+-\_.]+@[\w]+\.[\w]+$"
            regex_email = re.compile(email_reg)

            password_reg   = r"^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]$"
            regex_passowrd = re.compile(password_reg)

            if not regex_email.match(email) :
                return JsonResponse({'message':'Invalid Email'}, status=400)
            
            if User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'Aleady exists email'}, status=400)

            if len(password) < PASSWORD_LENGTH :
                return JsonResponse({'message':'Password Length Error'}, status=400)

            if not regex_passowrd.match(password) :
                return JsonResponse({'message':'Password regex error'}, status=400)
                
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

        except json.decoder.JSONDecodeError as msg :
            return JsonResponse({'message':msg})

class LoginView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
        
            if not User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'Account does not exists.'}, status=401)
            
            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')) :
                token = jwt.encode({'email':email, 'exp':timezone.now()+timedelta(weeks=3)}, SECRET_KEY, ALGORITHMS)
            
                return JsonResponse({'message':'SUCCESS', 'token':token}, status=200)
            
            return JsonResponse({'message':'Please check password'}, status=401)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError as msg :
            return JsonResponse({'message':msg})