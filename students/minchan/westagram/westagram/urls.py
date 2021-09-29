from django.urls import path

from users.views import UserRegister,UserLogin

urlpatterns = [
    path('users/register', UserRegister.as_view(), name='user_register'),
    path('users/login/', UserLogin.as_view(), name='user_login'),
]