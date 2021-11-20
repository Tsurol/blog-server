# Generated by Django 3.2.7 on 2021-11-16 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userprofile_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.CharField(blank=True, default='static/default_avatar.jpg', max_length=256, null=True, verbose_name='头像'),
        ),
    ]
