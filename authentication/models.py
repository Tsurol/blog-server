from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models, transaction
from django.contrib.auth.models import AnonymousUser
from authentication.choice import SexType
from utils.enums import Constants
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
            profile.nickname = profile.get_anonymous_username
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
    email = models.EmailField('邮箱地址', default=None, unique=True, null=True)
    # login_status = models.SmallIntegerField('登录状态', default=LoginStatusType.NOT_LOGIN, choices=LoginStatusType.choices)
    objects = AuthUserManager()

    class Meta:
        verbose_name = '用户基础信息'
        verbose_name_plural = '用户基础信息'
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def update_coins(self, amount, remark=None):
        """ 更新账户鲨币 """
        with transaction.atomic():
            if amount == 0:
                return
            # select_for_update来告诉数据库锁定对象，直到事务完成
            asset = UserAsset.objects.select_for_update().get(user=self)
            if asset.coins + amount < 0:
                raise Exception('鲨币余额不足')
            coins_before = asset.coins
            asset.coins += amount
            asset.save()
            coins_after = asset.coins
            UserCoinsRecord.objects.create(
                user=self, coins_changed=amount, coins_before=coins_before,
                coins_after=coins_after, reason=remark)


class UserProfile(models.Model):
    username = models.CharField('用户名', max_length=150, editable=False, default=None)
    nickname = models.CharField('昵称', max_length=255, default=None, null=True, blank=True)
    avatar = models.ImageField('头像', max_length=256, default='avatar/default_avatar.jpg', null=True, blank=True,
                               upload_to='avatar/%Y%m')
    sex = models.SmallIntegerField('性别', default=SexType.MAN, choices=SexType.choices)
    age = models.SmallIntegerField('年龄', default=0)
    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.OneToOneField(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='profile')

    class Meta:
        verbose_name = '用户详细信息'
        verbose_name_plural = '用户详细信息'
        db_table = 'auth_user_profile'

    def __str__(self):
        return self.username

    @property
    def get_anonymous_username(self):
        random_num = id_generator(7)
        return '{}{}'.format('匿名用户', random_num)


class LoginRecord(models.Model):
    username = models.CharField('用户名', max_length=150, editable=False, default=None)
    ip = models.CharField('IP地址', max_length=50, null=True, blank=True)
    source = models.CharField('登录来源', max_length=30, null=True, blank=True, default='web')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser,
                             on_delete=models.CASCADE, related_name='login_record')

    class Meta:
        db_table = 'auth_login_record'
        verbose_name = '登录历史'
        verbose_name_plural = '登录历史'

    def __str__(self):
        return self.username


class UserAsset(models.Model):
    username = models.CharField('用户名', max_length=150, editable=False, default=None)
    coins = models.IntegerField("账户鲨币", default=0)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.OneToOneField(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='asset')
    is_valid = models.BooleanField('逻辑删除', default=True)

    class Meta:
        db_table = 'auth_user_asset'
        verbose_name = '用户资产'
        verbose_name_plural = '用户资产'

    def __str__(self):
        return self.username


class UserCoinsRecord(models.Model):
    username = models.CharField('用户名', max_length=150, editable=False, default=None)
    coins_changed = models.IntegerField("鲨币变化数量", default=0)
    coins_before = models.IntegerField("鲨币变化前数量", default=0)
    coins_after = models.IntegerField("鲨币变化后数量", default=0)
    reason = models.CharField("备注信息", max_length=256, default=None, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='coins_record')

    class Meta:
        db_table = 'auth_user_coins_record'
        verbose_name = '鲨币交易记录'
        verbose_name_plural = '鲨币交易记录'

    def __str__(self):
        return self.username
