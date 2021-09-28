import json

from django.http import JsonResponse
from django.views import View

from .validations import *
from .models import User

class UserView(View):
    def post(self, request):
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
                
        try:            
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
            