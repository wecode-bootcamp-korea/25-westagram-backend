import json, re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            gender       = data['gender']
            date_birth   = data['date_birth']

            if password == '' or email == '':
                return JsonResponse({"message":"Email or Password cannot be empty"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"Email already exists"}, status=400)

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message':'Email format is not valid'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({'message':'Password format is not valid'}, status=400)

            if not re.match('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', date_birth): 
                return JsonResponse({'message':'Date format must be in YYYY-MM-DD'}, status=400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                gender       = gender,
                date_birth   = date_birth,
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)     

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
