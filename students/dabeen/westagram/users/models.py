from django.db import models


class User(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=100)
    web_site = models.CharField(max_length=100, null=True)
    information = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
