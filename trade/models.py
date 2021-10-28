from django.db import models

from authentication.models import AuthUser
from trade.choice import OrderStatus, PayType, GoodsStatus


class CommonModel(models.Model):
    is_valid = models.BooleanField('逻辑删除', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True


class Goods(CommonModel):
    name = models.CharField('商品名', max_length=64, default='鲨币')
    img = models.ImageField('商品图', upload_to='goods/%Y%m', max_length=512, default='avatar/coins.jpg')
    desc = models.CharField('简述', max_length=64, null=True, blank=True)
    price = models.FloatField('原价')
    discount = models.FloatField('折扣', default=10)
    total_stock = models.PositiveIntegerField('库存', default=0)
    remain_stock = models.PositiveIntegerField('剩余库存', default=0)
    status = models.SmallIntegerField('商品状态',
                                      choices=GoodsStatus.choices,
                                      default=GoodsStatus.OPEN)

    @property
    def sell_price(self):
        """ 销售价 = 原价 x 折扣 """
        return self.price * self.discount / 10

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        db_table = 'trade_goods'

    def __str__(self):
        return self.name


class Order(CommonModel):
    sn = models.CharField('订单号', max_length=128, unique=True)
    buy_count = models.IntegerField('购买商品数量', default=1)
    buy_amount = models.IntegerField('购买总金额')
    # 购买人的nickname
    to_user = models.CharField('客户', max_length=32)
    to_email = models.CharField('客户邮箱', max_length=128)
    remark = models.CharField('备注', max_length=64, null=True, blank=True)
    status = models.SmallIntegerField('订单状态',
                                      choices=OrderStatus.choices,
                                      default=OrderStatus.SUBMIT)
    goods = models.ForeignKey(verbose_name='关联商品', to=Goods, on_delete=models.PROTECT,
                              related_name='order_list')
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.PROTECT,
                             related_name='order_list')

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        db_table = 'trade_order'

    def __str__(self):
        return self.sn


class Payment(CommonModel):
    """ 支付凭证 """
    amount = models.FloatField('支付总金额', help_text='real pay')
    third_sn = models.CharField('第三方支付流水号', max_length=128, null=True, blank=True)
    pay_type = models.SmallIntegerField('支付方式', default=PayType.WECHAT, choices=PayType.choices)
    remark = models.CharField('备注信息', max_length=128, null=True, blank=True)
    user = models.ForeignKey(verbose_name='关联用户', to=AuthUser, on_delete=models.CASCADE, related_name='payment_list')
    order = models.OneToOneField(verbose_name='关联订单', to=Order, on_delete=models.CASCADE, related_name='payment_item')

    class Meta:
        verbose_name = '支付凭证'
        verbose_name_plural = '支付凭证'
        db_table = 'trade_payment'

    def __str__(self):
        return self.id
