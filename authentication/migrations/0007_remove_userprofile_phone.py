# Generated by Django 3.2.7 on 2021-09-24 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_authuser_login_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='phone',
        ),
    ]
