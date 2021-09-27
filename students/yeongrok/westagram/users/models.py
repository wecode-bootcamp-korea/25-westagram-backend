from django.db import models

class Users(models.Model):
    name        = models.CharField(max_length=200)
    email       = models.CharField(max_length=200)
    password    = models.CharField(max_length=200)
    mobile_num  = models.IntegerField()
    join_date   = models.DateTimeField()
    modify_date = models.DateTimeField()
    delete_date = models.DateTimeField()

    class Meta:
        db_table = "users"