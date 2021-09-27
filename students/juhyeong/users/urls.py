from django.urls import path
from users.views import SignUpsView

urlpatterns = [
    path('signup', SignUpsView.as_view()),
]