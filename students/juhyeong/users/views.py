import json
import re
import bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects

        if 'email' not in data:
            return JsonResponse({"message": "email_KEY_ERROR"}, status = 400)

        if 'password' not in data:
            return JsonResponse({"message": "password_KEY_ERROR"}, status = 400)

        if user.filter(email=data['email']).exists():
            return JsonResponse({"message": "이메일이 이미 등록되었습니다"}, status = 401)

        if not re.match('^[\w]+@[\w.\-]+\.[A-Za-z]{2,3}$', data['email']):
            return JsonResponse({"message": "이메일 형식이 잘못 되었습니다"}, status = 401)
        
        if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}$', data['password']):
            return JsonResponse({"message": "비밀번호 조건을 충족되지 않습니다"}, status =401)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user.create(
            name         = data['name'],
            email        = data['email'],
            password     = hashed_password,
            phone_number = data['phone_number'],
        )
        
        if data.get('profile'):
            user.last().profile = data['profile']

        return JsonResponse({'CREATED' : 'SUCCESS'}, status = 201)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = data['email'])

            if not (user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8'))):
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message" : "KeyError"}, status = 400)


        encoded_jwt = jwt.encode({'user' : user.id}, SECRET_KEY, algorithm = 'HS256')

        return JsonResponse({'access_token' : encoded_jwt}, status = 201)