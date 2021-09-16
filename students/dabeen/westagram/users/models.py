from django.db import models


class User(models.Model):
    # 이름, 이메일, 비밀번호, 연락처, 휴대폰, 그 외 개인정보
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    phone = models.IntegerField()
    web_site = models.CharField(max_length=100, null=True)
    information = models.TextField(null=True)

    class Meta:
        db_table = 'users'
