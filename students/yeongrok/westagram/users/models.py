from django.db import models

class User(models.Model): #꼭 단수표기
    name        = models.CharField(max_length=200)
    email       = models.CharField(max_length=200, unique=True)
    password    = models.CharField(max_length=200)
    mobile_num  = models.IntegerField()
    created_at   = models.DateTimeField()
    update_at = models.DateTimeField()
    deleted_at = models.DateTimeField()

    class Meta:
        db_table = "users" #복수표기