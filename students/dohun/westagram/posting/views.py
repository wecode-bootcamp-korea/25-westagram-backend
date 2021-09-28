import json

from django.http  import JsonResponse
from django.views import View
from .models      import Posting

class PostingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            Posting.objects.create(
                user      = data['user'],
                image     = data['image_url'],
                post_time = data['post_time']
            )

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
    
    def get(self, request):
        information = []

        postings = Posting.objects.all()

        for posting in postings:
            information.append(posting)

        return JsonResponse({'MESSAGE': information}, status=200)