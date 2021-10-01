import json
import jwt
import bcrypt

from django.http    import JsonResponse
from django.views   import View

from .validations   import validate_email, validate_password
from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user_email = data['email']
            user_pw    = data['password']
            

            if not validate_email(user_email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if not validate_password(user_pw):                
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
                    
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message' : 'DUPLICATED_EMAIL'}, status=400)

            encoded_pw  = user_pw.encode('utf-8')
            salt        = bcrypt.gensalt()
            hashed_pw   = bcrypt.hashpw(encoded_pw, salt)
            
            if bcrypt.checkpw(encoded_pw, hashed_pw):
                user    = User.objects.create(
                        name            = data['name'],
                        email           = data['email'],
                        password        = hashed_pw.decode('utf-8'),
                        phone_number    = data['phone_number'],
                        date_of_birth   = data.get('date_of_birth'),
                )

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class LoginView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user_email  = data['email']
            user_pw     = data['password']
            user        = User.objects.get(email=user_email)
            token       = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

            if not bcrypt.checkpw(user_pw.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status = 401,)
            
            return JsonResponse({"message": "SUCCESS", "access_token" : token}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400) 

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400) 