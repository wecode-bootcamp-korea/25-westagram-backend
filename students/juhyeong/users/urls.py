from django.urls import path
from users.views import SignUpsView, LoginsView

urlpatterns = [
    path('/signup', SignUpsView.as_view()),
    path('/login', LoginsView.as_view()),
]