from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=30)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30, null=True)
    hobby        = models.TextField(max_length=50, null=True)
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name