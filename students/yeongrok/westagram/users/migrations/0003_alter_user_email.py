# Generated by Django 3.2.7 on 2021-09-28 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210928_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
