# Generated by Django 3.2.7 on 2021-11-20 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default_avatar.jpg', max_length=300, null=True, upload_to='avatar/%Y/%m/%d', verbose_name='头像地址'),
        ),
    ]
