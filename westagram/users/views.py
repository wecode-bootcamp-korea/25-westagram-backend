import json

from django.http import JsonResponse
from django.views import View

from .validations import validate_email, validate_password
from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if 'password' not in data or 'email' not in data:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            if not validate_email(data['email']):
                return JsonResponse({
                    'Validation_Error' : '이메일은 @와 .가 포함된 이메일 형식이어야 합니다.'
                }, status = 400)

            if not validate_password(data['password']):
                return JsonResponse({
                    'Validation_Error' : '비밀번호는 8자리 이상으로 숫자, 문자, 특수기호가 하나 이상 포함되어야 합니다.'
                }, status = 400)
                    
            if not User.objects.filter(email=data['email']):
                user = User.objects.create(
                    name            = data['name'],
                    email           = data['email'],
                    password        = data['password'],
                    phone_number    = data['phone_number'],
                    date_of_birth   = data.get('date_of_birth'),
                )
            else:
                return JsonResponse({'message' : '중복된 이메일입니다.'}, status=400)

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if 'email' not in data or 'password' not in data:
                raise KeyError
            
            if not User.objects.filter(email=data['email']):
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            if User.objects.get(email=data['email']).password != data['password']:
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            else:
                return JsonResponse({"message": "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)