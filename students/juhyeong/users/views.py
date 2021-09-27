import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignUpsView(View):
    def post(self, request):
        data             = json.loads(request.body)
        email_checker    = re.compile('^[\w]+@[\w.\-]+\.[A-Za-z]{2,3}$')
        password_checker = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}$')
        user             = User.objects

        if 'email' not in data or 'password' not in data:
            return JsonResponse({"message": "KEY_ERROR"}, status =400)

        if user.filter(email=data['email']).exists():
            return JsonResponse({"message": "이메일이 이미 등록되었습니다"}, status =401)

        elif not email_checker.match(data['email']) != None:
            return JsonResponse({"message": "이메일 형식이 잘못 되었습니다"}, status =401)
        
        elif len(data['password']) < 8 or not password_checker.match(data['password']) != None:
            return JsonResponse({"message": "비밀번호 조건을 충족되지 않습니다"}, status =401)

        user.create(
            name         = data['name'],
            email        = data['email'],
            password     = data['password'],
            phone_number = data['phone_number'],
            profile      = data['profile']
        )
        return JsonResponse({'CREATED':'SUCCESS'}, status = 201)