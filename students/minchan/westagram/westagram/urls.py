from django.urls import path

from users.views import UserRegister

urlpatterns = [
    path('user/', UserRegister.as_view(), name='user_register'),
]