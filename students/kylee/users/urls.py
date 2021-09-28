from django.urls import path
from users.views import *

#localhost:8000/users
urlpatterns = [
    path('signup', SignupView.as_view())
]
