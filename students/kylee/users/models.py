from django.db            import models
from users.validator      import (
    email_validate,
    password_validate
)

class User(models.Model) :
    name       = models.CharField(max_length=50)
    email      = models.EmailField(max_length=50, unique=True, validators=[email_validate])
    password   = models.CharField(max_length=500, validators=[password_validate])
    telephone  = models.CharField(max_length=15)
    birthday   = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        db_table = 'users'