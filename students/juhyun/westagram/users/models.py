from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=120)
    password = models.CharField(max_length=300)
    username     = models.CharField(max_length=50, null=True)
    phone_number    = models.CharField(max_length=50, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'users'