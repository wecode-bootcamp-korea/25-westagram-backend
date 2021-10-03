import re
import jwt
import json
import bcrypt
from django.shortcuts import render

from django.views     import View
from django.db.models import Q
from django.http      import JsonResponse

from json.decoder import JSONDecodeError
from django.http      import JsonResponse
from .models    import User
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data=json.loads(request.body)
            
            email=data['email']
            password=data['password']

            if User.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)
            
            
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)
            if not re.match('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
    	        return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)
       
            
            User.objects.create(
                email         = email,
                phone_number  = data['phone_number'],
                username      = data['username'],
                password      = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
           try:
               data=json.loads(request.body)
               
               if not ('email' in data and 'password' in data):
                   return JsonResponse({'message':'KEY_ERROR'}, status=400)
                
               if not User.objects.filter(email=data['email']):
                   return JsonResponse({'message' : 'INVALID_USER'}, stauts=401)
               
               if User.objects.get(email=data['email']).password != data['password']:
                   return JsonResponse({'message' : 'INVALID_USER'}, stauts=401)
               
               return JsonResponse({'message' : 'LOGIN SUCCESS'}, status=200)
           
           except JSONDecodeError:
               return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
               
        

        