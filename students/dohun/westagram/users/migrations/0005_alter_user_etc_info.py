# Generated by Django 3.2.7 on 2021-09-28 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_etc_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='etc_info',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
