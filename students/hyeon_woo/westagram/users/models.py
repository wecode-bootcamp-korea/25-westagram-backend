from django.db import models

class User(models.Model):
    name          = models.CharField(max_length=50)
    email         = models.CharField(max_length=200)
    password      = models.CharField(max_length=50)
    phone_number  = models.CharField(max_length=50)
    information   = models.CharField(max_length=255)

    class Meta:
        db_table = "users"



