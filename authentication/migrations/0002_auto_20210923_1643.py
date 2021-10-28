# Generated by Django 3.2.7 on 2021-09-23 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
        migrations.AlterModelTable(
            name='authuser',
            table='auth_user',
        ),
    ]
