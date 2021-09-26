import json

from django.http        import JsonResponse
from django.views       import View

from users.validation   import validate_email, validate_password
from users.models       import User


class SignUp(View):
	def post(self, request):
		try:
			data = json.loads(request.body)

			name = data['name']
			email = data['email']
			password = data['password']
			other_info = data['other_info']
			phone_number = data['phone_number']

			if validate_email(email) == False:
					return JsonResponse({'MESSAGE':'INVALID_EMAIL_ADDRESS'}, status=400)
			
			if validate_password(password) == False:
					return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)
			
			if User.objects.filter(email = email).exists():
					return JsonResponse({'MESSAGE' : 'ALREADY_EXISTS_EMAIL'}, status=400)

			User.objects.create(
					name = name,
					email = email,
					password = password,
					other_info = other_info,
					phone_number = phone_number
			)

			return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)
			
		except KeyError:
			return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)


class SignIn(View):
	def get(self, request):
		data = json.loads(request.body)
		try :
			email = data['email']
			password = data['password']

			if not User.objects.filter(email = email).exists():
					return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 401)
			
			if not User.objects.get(email = email).password == password:
					return JsonResponse({'MESSAGE':'INVALIED_USER'}, status = 401)
			
			return JsonResponse({'MESSGAE' : 'SUCCESS'}, status = 200)

		except KeyError :
			return JsonResponse({'MESSAGE' : "KEY_ERROR"}, status = 400)