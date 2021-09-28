import jwt

from users.models import User
from django.http  import JsonResponse

from my_settings import (
    MY_ALGORITMS,
    MY_SECRET_KEY
)

def login_decorator(func) :
    def wrapper(self, request, *args, **kwrags) :
        try :
            token = request.headers.get('Authorization', None)
            payload = jwt.decode(token, MY_SECRET_KEY, MY_ALGORITMS)
            login_user = User.objects.get(email=payload['email'])
            request_user = login_user
        
        except jwt.exceptions.DecodeError :
            return JsonResponse({'message':"Invalid token type. Token must be a <class 'bytes'>"}, status=401)
        
        except jwt.ExpiredSignatureError :
            return JsonResponse({'message':"Expired Token"}, status=401)
        
        return func(self, request, *args, **kwrags)
    
    return wrapper