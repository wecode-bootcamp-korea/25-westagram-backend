from django.db import models

# Create your models here.

class Users(models.Model) :
    name            = models.CharField(max_length=45)
    email           = models.CharField(max_length=200,null=True)
    password        = models.CharField(max_length=45)
    phone_number    = models.CharField(max_length=13, default="010-0000-0000")
    profile_etc     = models.TextField(null=True)
