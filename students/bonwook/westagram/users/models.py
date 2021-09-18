from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=100, blank=False)
    email           = models.EmailField(
        max_length  = 200, 
        unique      = True, 
        blank       = False     
    )
    password        = models.CharField(max_length=200, blank=False)
    phone_number    = models.CharField(
        max_length  = 45,
        unique      = True, 
        blank       = False
    )
    date_of_birth   = models.DateField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table    = 'users'