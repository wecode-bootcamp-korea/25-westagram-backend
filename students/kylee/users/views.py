import json
import re

from django.views import View
from django.http  import JsonResponse
from users.models import *

class SignupView(View) :
    def post(self, request) :
        data = json.loads(request.body)

        try :

            email     = data.get('email',    None)
            password  = data.get('password', None)
            birthday  = data.get('birthday', None)

            if not email or not password :

                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if email :
                if not re.match('^[\w+-\_.]+@[\w]+\.[\w]+$', email) :
                    return JsonResponse({'ValidationError':'이메일은 @ 와 . 이 형식에 맞게 순서대로 들어가야 합니다.'}, status=400)

                if Users.objects.filter(email=email).exists() :
                    return JsonResponse({'message':'기존재 이메일입니다.'}, status=400)

            if password :
                if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$', password) :
                    return JsonResponse({'ValidationError':'비밀번호에는 숫자/문자/특수문자가 1개씩 들어가야 합니다.'}, status=400)

            Users.objects.create(
                email     = email,
                password  = password,
                name      = data['name'],
                telephone = data['telephone'],
                birthday  = birthday
            )

            return JsonResponse({'mesage':'SUCCESS'},status=201)
        
        except Exception as msg :
            return JsonResponse({'message':msg}, status=400)