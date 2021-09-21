from django.urls import path
from users.views import LoginView

urlpatterns = [
        path('/signup', LoginView.as_view()),
]