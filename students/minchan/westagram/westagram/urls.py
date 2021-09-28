from django.urls import path

from users.views import UserRegister,UserLogin

urlpatterns = [
    path('user/', UserRegister.as_view(), name='user_register'),
    path('user_login/', UserLogin.as_view(), name='user_register'),
]