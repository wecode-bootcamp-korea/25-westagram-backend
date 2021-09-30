from django.db import models

# Create your models here.
class User(models.Model):
    name        = models.CharField(max_length=45)
    email       = models.EmailField(unique=True)
    password    = models.CharField(max_length=100)
    contact     = models.CharField(max_length=100, null=True, default='')
    other_info  = models.CharField(max_length=100, null=True, default='')


    class Meta:
        db_table = 'users'
