from django.db            import models

# Create your models here.
class Users(models.Model) :
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, primary_key=True)
    password = models.CharField(max_length=500)
    tel = models.CharField(max_length=15)
    birthday = models.DateField()

    class Meta :
        db_table = 'users'