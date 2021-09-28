from django.views import View
from django.http  import JsonResponse
from users.models import *

import json, re

class SignupView(View) :
    def post(self, request) :
        #email / password / name / telephone / birthday(단, 생일은 필수값 아님)
        data = json.loads(request.body)

        try :

            data_email     = data.get('email',None)
            data_password  = data.get('password', None)
            data_birthday  = data.get('birthday',None)

            if not data_email or not data_password :

                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            
            if data_email :
                if not re.match('^[\w+-\_.]+@[\w]+\.[\w]+$', data_email) :
                    return JsonResponse({'ValidationError':'이메일은 @ 와 . 이 형식에 맞게 순서대로 들어가야 합니다.'}, status=400)

                if Users.objects.filter(email=data_email).exists() :
                    return JsonResponse({'message':'기존재 이메일입니다.'}, status=400)

            if data_password :
                if not re.match('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=-])[a-zA-Z0-9!@#$%^&*()_+=-]{8,}$', data_password) :
                    return JsonResponse({'ValidationError':'비밀번호에는 숫자/문자/특수문자가 1개씩 들어가야 합니다.'}, status=400)

            Users.objects.create(
                email     = data_email,
                password  = data_password,
                name      = data['name'],
                telephone = data['telephone'],
                birthday  = data_birthday
            )

            return JsonResponse({'mesage':'SUCCESS'},status=201)
        
        except Exception as msg :
            return JsonResponse({'message':msg}, status=400)