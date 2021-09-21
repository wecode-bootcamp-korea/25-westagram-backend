import json
import re

from django.http import JsonResponse
from django.views import View
from .models import User


class LoginView(View):
    def post(self, request):

        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        try:
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status = 401)

            user = User.objects.get(email = email)

            if user.password != password:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status = 401)
            
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)

        
        except KeyError:
            return JsonResponse({'MESSAGE': 'Key_Error'}, status = 401)