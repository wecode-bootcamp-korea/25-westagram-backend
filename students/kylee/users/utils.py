import jwt

from users.models       import User
from django.http        import JsonResponse

from westagram.settings import (
    ALGORITHMS,
    MY_SECRET_KEY
)

def login_decorator(func) :
    def wrapper(self, request) :
        try :
            token   = request.headers.get('Authorization', None)
            payload = jwt.decode(token, MY_SECRET_KEY, ALGORITHMS)
            user    = User.objects.get(email=payload['email'])
            
        except jwt.exceptions.DecodeError :
            return JsonResponse({'message':"Invalid token type. Token must be a <class 'bytes'>"}, status=401)
        
        except jwt.ExpiredSignatureError :
            return JsonResponse({'message':"Expired Token"}, status=401)
        
        return func(self, request)
    
    return wrapper