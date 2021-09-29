import json, re, bcrypt, jwt

from django.http        import JsonResponse
from django.views       import View

from users.models       import User

from my_settings		import SECRET_KEY, ALGORITHM


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            other_info   = data['other_info']
            phone_number = data['phone_number']

            email_regex    = "^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            password_regex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"

            if not re.match(email_regex, email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)

            if not re.match(password_regex, password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_password, # 생성하는 비밀번호가 디코드된 비밀번호이어야 함!
                other_info   = other_info,
                phone_number = phone_number
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try :
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
				
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode(
						{'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM # 이부분 이해해야함. 시크릿키는 my_settings.py에 있는 것
					)

                    return JsonResponse({'access_token' : access_token}, status=200)

                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'MESSAGE' : 'INVALID_USER_EMAIL'}, status=401)

        except KeyError :
            return JsonResponse({'MESSAGE' : "KEY_ERROR"}, status = 400)