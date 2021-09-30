from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    other_information = models.TextField(max_length=1000, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
