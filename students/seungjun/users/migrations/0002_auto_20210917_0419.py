# Generated by Django 3.2.7 on 2021-09-17 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date_joined',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='date_modified',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(help_text='000-0000-0000', max_length=15),
        ),
    ]
