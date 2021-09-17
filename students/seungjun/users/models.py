from django.db import models

# Create your models here.

class User (models.Model):

    name          = models.CharField(max_length=100)
    email         = models.EmailField(max_length=100, unique=True)
    password      = models.CharField(max_length=100)
    phone_number  = models.CharField(max_length=15, help_text="000-0000-0000")
    gender        = models.CharField(max_length=10, null=True)
    date_birth    = models.DateField(null=True)
    updated_at    = models.DateField(auto_now=True)
    created_at    = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'users'