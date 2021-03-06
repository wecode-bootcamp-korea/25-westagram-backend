from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=45, null=True)
    email        = models.CharField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100, default='')
    other_info   = models.CharField(max_length=300, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table    = "users"