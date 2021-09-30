from django.urls import path
from posting.views import PostView, GetPostView, CommentView, GetCommentView, LikeView

urlpatterns = [
        path('post', PostView.as_view()),
        path('getpost', GetPostView.as_view()),
        path('comment', CommentView.as_view()),
        path('getcomment', GetCommentView.as_view()),
        path('like', LikeView.as_view())
] 