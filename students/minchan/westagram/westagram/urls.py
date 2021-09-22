from django.urls import path
from users.views import user_register,user_login

urlpatterns = [
    path('minchan/user_register', user_register.as_view(), name='user_register'),
    path('minchan/user_login', user_login.as_view(), name='user_login'),
]