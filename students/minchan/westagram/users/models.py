from django.db import models
class Users(models.Model) :
    name            = models.CharField(max_length=45)
    email           = models.CharField(max_length=200,unique=True)
    password        = models.CharField(max_length=200)
    phone_number    = models.CharField(max_length=13, default="010-0000-0000")
    profile_etc     = models.TextField(null=True)
    created_at      = models.DateField(auto_now_add=True)
    updated_at      = models.DateField(auto_now=True)

    class Meta :
        db_table = "users"