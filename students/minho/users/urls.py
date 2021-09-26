from django.urls    import path
from users.views    import SignIn, SignUp

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/signin', SignIn.as_view()), 
]
	# 클래스 뷰를 만들고 여기다가 연결을 해줘야 함!