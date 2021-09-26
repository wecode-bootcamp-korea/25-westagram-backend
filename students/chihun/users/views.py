import json
from json.decoder           import JSONDecodeError
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError


from users.validation       import validate_email, validate_password
from users.models           import User

class SignUp(View):
    def post(self, request):
        try :
            data         = json.loads(request.body)
            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            blog_url     = data.get('blog_url')  # null = True

            validate_email(email)
            validate_password(password)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_EMAIL'}, status=400)
            
            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
                blog_url     = blog_url,
            )

            return JsonResponse({'MESSAGE':'SUCCESS'} , status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status = 400)
        
        except ValidationError as e:
            return JsonResponse({'MESSAGE':(e.message)}, status=400)
        
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)
