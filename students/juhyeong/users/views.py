import json
import re
import bcrypt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY

class SignUpsView(View):
    def post(self, request):
        data             = json.loads(request.body)
        email_checker    = re.compile('^[\w]+@[\w.\-]+\.[A-Za-z]{2,3}$')
        password_checker = re.compile('^(?=.*[A-Za-z])(?=*\d)(?=.*[~!@#$^&*()+|=])[(A-Za-z\d~!@#$%^&*+|=)]{8,}$')
        user             = User.objects

        if 'email' or 'data' not in data:
            return JsonResponse({"message": "KEY_ERROR"}, status =400)

        if user.filter().exists():
            return JsonResponse({"message": "KEY_ERROR"}, status =401)

        elif not email_checker.match(data['email']) != None:
            return JsonResponse({"message": "이메일 형식이 잘못 되었습니다"}, status =401)
        
        elif len() < 8 or not password_checker.match(data['password']) != None:
            return JsonResponse({"message": "비밀번호 조건을 충족되지 않습니다"}, status =401)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        user.create(
            name         = data['name'],
            email        = data['email'],
            password     = hashed_password.decode('utf-8'),
            phone_number = data['phone_number'],
            profile      = data['profile']
        )
        return JsonResponse({'CREATED':'SUCCESS'}, status = 201)