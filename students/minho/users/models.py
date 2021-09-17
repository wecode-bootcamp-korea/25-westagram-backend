from django.db      import models

class User(models.Model):
    name            = models.CharField(max_length=45)
    email           = models.CharField(max_length=45, unique=True)
    password        = models.CharField(max_length=45)
    phone_number    = models.IntegerField
    other_info      = models.CharField(max_length=300, null=True)

    class Meta:
        db_table    = "users"