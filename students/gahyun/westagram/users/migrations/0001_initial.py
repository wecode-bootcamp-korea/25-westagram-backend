# Generated by Django 3.2.7 on 2021-09-27 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('user_email', models.EmailField(max_length=50, unique=True)),
                ('user_password', models.CharField(max_length=50)),
                ('user_phone_num', models.CharField(max_length=30, unique=True)),
                ('user_hobby', models.TextField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
