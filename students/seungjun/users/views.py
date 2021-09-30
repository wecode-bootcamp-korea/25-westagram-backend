import json, re, bcrypt, jwt
from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View

from users.models       import User
from westagram.settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            gender       = data['gender']
            date_birth   = data.get('date_birth')
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"Email already exists"}, status=400)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message':'Email format is not valid'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({'message':'Password format is not valid'}, status=400)
            
            if date_birth is not None:
                if not re.match('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', date_birth): 
                    return JsonResponse({'message':'Date format must be in YYYY-MM-DD'}, status=400)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = decoded_password,
                phone_number = phone_number,
                gender       = gender,
                date_birth   = date_birth,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)     

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({'access_token': token,'message':'SUCCESS'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_EMAIL'}, status=401)
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)