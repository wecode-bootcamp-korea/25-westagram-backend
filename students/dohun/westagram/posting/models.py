from django.db    import models
from users.models import User

class Posting(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    post_time  = models.DateTimeField(auto_now_add=True)
    image      = models.URLField(max_length=1000)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    post         = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment      = models.CharField(max_length=500)

    class Meta:
        db_table = 'comments'