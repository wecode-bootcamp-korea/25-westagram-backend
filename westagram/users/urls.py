from django.urls    import path
from users.views    import SignUpView, SignInView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signup', SignInView.as_view()),
]