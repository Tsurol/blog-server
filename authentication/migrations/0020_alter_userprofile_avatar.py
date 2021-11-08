# Generated by Django 3.2.7 on 2021-11-08 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0019_alter_userasset_coins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='static/default_avatar.jpg', max_length=256, null=True, upload_to='userAvatar/%Y%m', verbose_name='头像'),
        ),
    ]