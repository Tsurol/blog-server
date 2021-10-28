from django.db import models


class GoodsStatus(models.IntegerChoices):
    OPEN = 1, '开放购买'
    CLOSED = 0, '暂未开放'


class OrderStatus(models.IntegerChoices):
    SUBMIT = 11, '待支付'
    PAID = 12, '已支付'
    CANCELED = 13, '已取消'


class PayType(models.IntegerChoices):
    WECHAT = 1
    ZFB = 2
