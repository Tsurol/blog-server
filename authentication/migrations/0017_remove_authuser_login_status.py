# Generated by Django 3.2.7 on 2021-10-25 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_auto_20210928_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authuser',
            name='login_status',
        ),
    ]
