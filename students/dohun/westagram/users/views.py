import json
import re

from django.http import JsonResponse
from django.views import View
from .models import User

class UserView(View):
    def post(self, request):

        data               = json.loads(request.body)
        password_check     = data['password']
        email_check        = data['email']

        try:
            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email_check):
                return JsonResponse({'MESSAGE' : 'RETYPE_EMAIL'}, status=400)

            if not re.match('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}', password_check):
                return JsonResponse({'MESSAGE' : 'RETYPE_PASSWORD'}, status=400)

            if User.objects.filter(email=email_check).exists():
                return JsonResponse({'MESSAGE' : 'EXISTING_EMAIL'}, status=400)

            User.objects.create(
                name           = data['name'],
                email          = email_check,
                password       = password_check,
                phone_number   = data['phone_number'],
                etc_info       = data['etc_info']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
