# Generated by Django 3.2.7 on 2021-09-27 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('mobile_num', models.IntegerField()),
                ('join_date', models.DateTimeField()),
                ('modify_date', models.DateTimeField()),
                ('delete_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]