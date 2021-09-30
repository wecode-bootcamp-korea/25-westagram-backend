import json

from django.http  import JsonResponse
from django.views import View
from .models      import Posting, Comment, Like
from users.models import User

class PostView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_email = data['user']
            user = User.objects.get(email=user_email)

            if User.objects.filter(email = user_email).exists():
                Posting.objects.create(
                    user       = user,
                    image      = data['image']
                )
                return JsonResponse({'MESSAGE' : 'CREATED'}, status=201)

            return JsonResponse({'MESSAGE': 'NONEXISTING_USER'}, status=400)        

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
    
class GetPostView(View):
    def get(self, request):
        information = []
        postings = Posting.objects.all()

        for posting in postings:
            
            information.append(
                {
                    'post_time': posting.post_time,
                    'image': posting.image,
                    'user': posting.user.name
                }
            )

        return JsonResponse({'MESSAGE': information}, status=200)

class CommentView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            comment    = data['comment']
            user_email = data['user']
            post_id    = data['post']

            post = Posting.objects.get(id=post_id)
            user = User.objects.get(email=user_email)
            
            if not User.objects.filter(email = user_email).exists():
                return JsonResponse({'MESSAGE': 'NONEXISTING_USER'}, status=400)
            
            if not Posting.objects.filter(id=post_id).exists():
                return JsonResponse({'MESSAGE': 'NONEXISTING_POST'}, status=400)

            Comment.objects.create(
                post    = post,
                user    = user,
                comment = comment
            )
            return JsonResponse({'MESSAGE': 'COMMENTED'}, status=201)

        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class GetCommentView(View):
    def get(self, request):
        try:
            posts        = Posting.objects.all()
            all_comments = []

            for post in posts:
                post_comments = []
                comments      = post.comment_set.all()

                for comment in comments:
                    post_comments.append(comment.comment)
                
                all_comments.append(post_comments)
            
            return JsonResponse({'MESSAGE': all_comments[0]}, status=201)

        except:
            JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LikeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_email = data['user']
            post_id = data['post']

            post = Posting.objects.get(id=post_id)
            user = User.objects.get(email=user_email)

            if not Like.objects.filter(post=post, user=user).exists():
                Like.objects.create(
                    post = post,
                    user = user
                )
                return JsonResponse({'MESSAGE': 'LIKE_SUCCESS'}, status=201)
            
            return JsonResponse({'SUCCESS': 'ALREADY_LIKED'}, status=400)

        except:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)