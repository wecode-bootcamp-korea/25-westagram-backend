import json
import jwt

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def login_checker(func):

    def wrapper(self, request):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user_id      = User.objects.get(id=payload['id'])
            request.user = user_id

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        return func(self, request)

    return wrapper