from trade.models import Order
from trade.serializers import OrderSerializer
from utils.enums import RespCode
from utils.pagination import MyPagination
from utils.verify import current_user


def order_submit(goods_id, buy_count, to_phone, to_user, request):
    pass


def get_order_detail(request, sn):
    pass


def order_delete(request, sn):
    pass


def order_cancel(request, sn):
    pass


def order_pay_submit(request, sn):
    pass


def get_order_list(request, status):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    order_ls = Order.objects.filter(is_valid=True, user=user, status=status)
    if not order_ls:
        return RespCode.NO_CONTENT.value, {}, []
    page_obj = MyPagination()
    page_res = page_obj.paginate_queryset(queryset=order_ls, request=request)
    order_data = OrderSerializer(page_res, many=True).data
    return RespCode.OK.value, order_data
