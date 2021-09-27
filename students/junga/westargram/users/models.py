from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=100)
    user_pw = models.CharField(max_length=100)
    user_tel = models.IntegerField()
    user_info = models.TextField(max_length=1000)

    class Meta:
        db_table = 'users'