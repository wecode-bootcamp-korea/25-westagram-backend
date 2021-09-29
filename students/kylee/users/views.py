import bcrypt
import json
import jwt

from django.views           import View
from django.utils           import timezone
from django.http            import JsonResponse
from users.models           import User
from django.core.exceptions import ValidationError
from my_settings            import MY_ALGORITMS, MY_SECRET_KEY
from datetime               import timedelta

#python manage.py runserver 0:8000

#10.58.4.21:8000/users/signup 
class SignupView(View) :
    def post(self, request) :

        try :

            data = json.loads(request.body)
            print(data)

            name      = data.get('name', None)
            telephone = data.get('telephone', None)
            email     = data['email']
            password  = data['password']
            birthday  = data.get('birthday', None)
            
            if User.objects.filter(email=email).exists() :
                print(User.objects.filter(email=email))
                return JsonResponse({'message':'기존재 이메일입니다.'}, status=400)
                
            user = User.objects.create(
                email     = email,
                password  = password,
                name      = name,
                telephone = telephone,
                birthday  = birthday
            )
            
            print(user)

            user.full_clean()

            print(1)
            
            user.password = user.password.encode('utf-8')
            user.password = bcrypt.hashpw(user.password, bcrypt.gensalt())
            user.password = user.password.decode('utf-8')

            print(2)

            user.save()
            
            print(3)
            
            return JsonResponse({'mesage':'SUCCESS'},status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except ValidationError as msg :
            if User.objects.filter(email=email).exists() :
                User.objects.filter(email=email).delete()

            messages = ''

            for message in msg.messages :
                messages += message

            return JsonResponse({'message':messages}, status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({'message':'값을 하나라도 입력해주세요'})

#10.58.4.21:8000/users/login
class LoginView(View) :
    def post(self, request) :
        try :
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']
        
            if not User.objects.filter(email=email).exists() :
                return JsonResponse({'message':'Account does not exist'}, status=401)
            
            user = User.objects.get(email=email)

            inputed_password = password.encode('utf-8')
            db_password      = user.password.encode('utf-8')

            if bcrypt.checkpw(inputed_password, db_password) :

                token = jwt.encode({'email':email, 'exp':timezone.now()+timedelta(weeks=3)}, MY_SECRET_KEY, MY_ALGORITMS)
            
                return JsonResponse({'message':'SUCCESS', 'token':token}, status=200)
            
            return JsonResponse({'message':'Unauthorized'}, status=401)

        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except json.decoder.JSONDecodeError :
            return JsonResponse({'message':'값을 하나라도 입력해주세요'})