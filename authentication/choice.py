from django.db import models


class SexType(models.IntegerChoices):
    MAN = 11, '男'
    WOMAN = 12, '女'


# class LoginStatusType(models.IntegerChoices):
#     """
#     LoginStatusType.choices:
#     [(1, '登陆中'), (0, '未登录')]
#     """
#     LOGGING = 1, '登陆中'
#     NOT_LOGIN = 0, '未登录'
