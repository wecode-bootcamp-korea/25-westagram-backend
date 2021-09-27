from django.db import models

# unique=true로 설정하면 data는 db안에서 유일해야 하게 됨.
# null=true는 입력하지 않아도 되는 field라는 의미.(기본값으로 false)
class User(models.Model):
    user_name        = models.CharField(max_length=30)
    user_email       = models.EmailField(max_length=50, unique=True)
    user_password    = models.CharField(max_length=50)
    # pip install django-phonenumber-field[phonenumberslite] 설치오류로 우선 CF씀.
    user_phone_num   = models.CharField(max_length=30, unique=True)
    user_hobby  = models.TextField(max_length=50, null=True)

    # Meta options: https://docs.djangoproject.com/ko/3.2/topics/db/models/#meta-options
    class Meta:
        db_table = 'users'

    # model methods: https://docs.djangoproject.com/ko/3.2/topics/db/models/#model-methods
    def __str__(self):
        return self.user_name