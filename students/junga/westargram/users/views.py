import json, re

from django.http    import JsonResponse
from django.views   import View

from users.models   import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message' : 'ERROR_EMAIL_ALREADY_EXIST'}, status=400)

            if (data['email'] == '') or (data['password'] == ''):
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400) 
           
            #if not re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            
            #if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", data["password"]):
                return JsonResponse({"message": "INVALID_PASSWORD)"}, status=400)
            
            User.objects.create(
                name = data['name'],
                email = data['email'],
                password = data['password'],
                phone_number = data['phone_number'],
                other_information = data.get('other_informaion')
            )
            return JsonResponse({'message' : 'SUCCESS'} , status = 201)
        
        except Exception:
            return JsonResponse({'message' : 'FAILED'}, status=400)