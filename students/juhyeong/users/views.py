import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignUpsView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects

        if 'email' not in data:
            return JsonResponse({"message": "KEY_ERROR" + ": email"}, status = 400)

        if 'password' not in data:
            return JsonResponse({"message": "KEY_ERROR"+":password"}, status = 400)

        if user.filter(email=data['email']).exists():
            return JsonResponse({"message": "이메일이 이미 등록되었습니다"}, status = 401)

        if not re.match('^[\w]+@[\w.\-]+\.[A-Za-z]{2,3}$', data['email']):
            return JsonResponse({"message": "이메일 형식이 잘못 되었습니다"}, status = 401)
        
        if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}$', data['password']):
            return JsonResponse({"message": "비밀번호 조건을 충족되지 않습니다"}, status =401)

        user.create(
            name         = data['name'],
            email        = data['email'],
            password     = data['password'],
            phone_number = data['phone_number'],
        )
        
        if data.get('profile'):
            user.last().profile = data['profile']

        return JsonResponse({'CREATED':'SUCCESS'}, status = 201)

class LoginsView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects

        if 'email' not in data:
            return JsonResponse({"message": "KEY_ERROR" + " : email"}, status = 400)

        if 'password' not in data:
            return JsonResponse({"message": "KEY_ERROR"+" : password"}, status = 400)

        if not user.filter(email=data['email']).filter(password = data['password']).exists():
            return JsonResponse({"message": "INVALID_USER"}, status = 401)

        return JsonResponse({'message':'SUCCESS'}, status = 200)