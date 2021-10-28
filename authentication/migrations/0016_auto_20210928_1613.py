# Generated by Django 3.2.7 on 2021-09-28 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_remove_usercoinsrecord_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userasset',
            name='is_valid',
            field=models.BooleanField(default=True, verbose_name='逻辑删除'),
        ),
        migrations.AlterField(
            model_name='usercoinsrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coins_record', to=settings.AUTH_USER_MODEL, verbose_name='关联用户'),
        ),
    ]