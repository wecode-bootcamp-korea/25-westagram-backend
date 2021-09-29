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
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not validate_password(data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                    
            if not User.objects.filter(email=data['email']):
                user = User.objects.create(
                    name            = data['name'],
                    email           = data['email'],
                    password        = data['password'],
                    phone_number    = data['phone_number'],
                    date_of_birth   = data.get('date_of_birth'),
                )
            else:
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status=400)

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if 'email' not in data or 'password' not in data:
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)
            
            if not User.objects.filter(email=data['email']):
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            if User.objects.get(email=data['email']).password != data['password']:
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            else:
                return JsonResponse({"message": "SUCCESS"}, status = 200)

        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)            