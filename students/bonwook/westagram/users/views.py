import json

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.views import View

from .models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.create(
            name            = data['name'],
            email           = data['email'],
            password        = data['password'],
            phone_number    = data['phone_number'],
            date_of_birth   = data['date_of_birth'], 
        )

        return HttpResponse({'MESSAGE' : 'CREATED'}, status = 201)
