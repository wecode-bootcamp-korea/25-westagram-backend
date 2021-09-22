from django.urls import path
from users.views import user_register

urlpatterns = [
    path('/user_register', user_register.as_view(), name='user_register'),
]