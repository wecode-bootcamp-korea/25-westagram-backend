import json

from django.http import JsonResponse
from django.views import View

from .validations import validate_email, validate_password
from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not ('password' in data and 'email' in data):
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            if not validate_email(data['email']):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not validate_password(data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                    
            if User.objects.filter(email=data['email']).exists():                
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status=400)

            user = User.objects.create(
                    name            = data['name'],
                    email           = data['email'],
                    password        = data['password'],
                    phone_number    = data['phone_number'],
                    date_of_birth   = data.get('date_of_birth'),
                )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not ('email' in data and 'password' in data):
                return JsonResponse({"message": "KEY_ERROR"}, status = 400)
            
            if not User.objects.filter(email=data['email']):
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            if User.objects.get(email=data['email']).password != data['password']:
                return JsonResponse({"message": "INVALID_USER"}, status = 401)

            return JsonResponse({"message": "SUCCESS"}, status = 200)

        except Exception as e:
            return JsonResponse({'message' : e}, status = 400)            