import random

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models, transaction
from django.contrib.auth.models import AnonymousUser
from authentication.choice import SexType
from utils.enums import Constants, VUE_HOST
from utils.id import id_generator, uid_gen


class AuthUserManager(BaseUserManager):
    def _create_user(self, password, **extra_fields):
        """
        Creates and saves a User with the given steamid and password.
        """
        with transaction.atomic():
            user = self.model(**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            profile = UserProfile.objects.create(user=user, username=user.username)
            profile.nickname = profile.get_anonymous_nickname
            profile.save()
            UserAsset.objects.create(user=user, coins=Constants.INIT_COINS.value, username=user.username)
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_anonymous_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(password, **extra_fields)


class AuthUser(AbstractUser):
    USERNAME_FIELD = 'username'
    email = models.EmailField('????????????', default=None, unique=True, null=True)
    # login_status = models.SmallIntegerField('????????????', default=LoginStatusType.NOT_LOGIN, choices=LoginStatusType.choices)
    objects = AuthUserManager()

    class Meta:
        verbose_name = '??????????????????'
        verbose_name_plural = '??????????????????'
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def update_coins(self, amount, remark=None):
        """ ?????????????????? """
        with transaction.atomic():
            if amount == 0:
                return
            # select_for_update???????????????????????????????????????????????????
            asset = UserAsset.objects.select_for_update().get(user=self)
            if asset.coins + amount < 0:
                raise Exception('??????????????????')
            coins_before = asset.coins
            asset.coins += amount
            asset.save()
            coins_after = asset.coins
            UserCoinsRecord.objects.create(
                user=self, coins_changed=amount, coins_before=coins_before,
                coins_after=coins_after, reason=remark)


class UserProfile(models.Model):
    username = models.CharField('?????????', max_length=150, editable=False, default=None)
    nickname = models.CharField('??????', max_length=255, default=None, null=True, blank=True)
    # avatar = models.CharField('??????', max_length=256, default=VUE_HOST + 'static/default_avatar.jpg', null=True,
    #                           blank=True)
    avatar = models.ImageField('????????????', max_length=300, null=True, blank=True, upload_to='avatar/%Y/%m/%d',
                               default='avatar/default_avatar.jpg')
    sex = models.SmallIntegerField('??????', default=SexType.MAN, choices=SexType.choices)
    age = models.SmallIntegerField('??????', default=0)
    words = models.CharField('????????????', max_length=64, null=True, blank=True, default='??????????????????????????????')
    is_valid = models.BooleanField('????????????', default=True)
    created_at = models.DateTimeField('????????????', auto_now_add=True)
    updated_at = models.DateTimeField('????????????', auto_now=True)
    user = models.OneToOneField(verbose_name='????????????', to=AuthUser, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = '??????????????????'
        verbose_name_plural = '??????????????????'
        db_table = 'auth_user_profile'

    def __str__(self):
        return self.avatar

    @property
    def get_anonymous_nickname(self):
        # random_num = id_generator(4)
        # return '{}{}'.format('??????????????????', random_num)
        random_num = id_generator(5)
        random_nickname = random.choice(['?????????', '?????????', '?????????', '?????????', '?????????'])
        return '{}{}'.format(random_nickname, random_num)


class LoginRecord(models.Model):
    username = models.CharField('?????????', max_length=150, editable=False, default=None)
    ip = models.CharField('IP??????', max_length=50, null=True, blank=True)
    source = models.CharField('????????????', max_length=30, null=True, blank=True, default='web')
    created_at = models.DateTimeField('????????????', auto_now_add=True)
    user = models.ForeignKey(verbose_name='????????????', to=AuthUser,
                             on_delete=models.CASCADE, related_name='login_record')

    class Meta:
        db_table = 'auth_login_record'
        verbose_name = '????????????'
        verbose_name_plural = '????????????'

    def __str__(self):
        return self.username


class UserAsset(models.Model):
    username = models.CharField('?????????', max_length=150, editable=False, default=None)
    coins = models.FloatField("????????????", default=0.0)
    updated_at = models.DateTimeField('????????????', auto_now=True)
    user = models.OneToOneField(verbose_name='????????????', to=AuthUser, on_delete=models.CASCADE, related_name='asset')
    is_valid = models.BooleanField('????????????', default=True)

    class Meta:
        db_table = 'auth_user_asset'
        verbose_name = '????????????'
        verbose_name_plural = '????????????'

    def __str__(self):
        return self.username


class UserCoinsRecord(models.Model):
    username = models.CharField('?????????', max_length=150, editable=False, default=None)
    coins_changed = models.IntegerField("??????????????????", default=0)
    coins_before = models.IntegerField("?????????????????????", default=0)
    coins_after = models.IntegerField("?????????????????????", default=0)
    reason = models.CharField("????????????", max_length=256, default=None, null=True, blank=True)
    created_at = models.DateTimeField('????????????', auto_now_add=True)
    updated_at = models.DateTimeField('????????????', auto_now=True)
    user = models.ForeignKey(verbose_name='????????????', to=AuthUser, on_delete=models.CASCADE, related_name='coins_record')

    class Meta:
        db_table = 'auth_user_coins_record'
        verbose_name = '??????????????????'
        verbose_name_plural = '??????????????????'

    def __str__(self):
        return self.username
