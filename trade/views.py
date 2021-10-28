from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from trade.bussiness import order_submit, get_order_detail, order_delete, order_cancel, order_pay_submit, get_order_list
from utils.enums import RespCode
from utils.response import reformat_resp


class OrderSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ 下订单 """
        try:
            goods_id = int(request.data.get('goods_id', None))
            buy_count = int(request.data.get('buy_count', None))
            to_phone = request.data.get('to_phone', None)
            to_user = request.data.get('to_user', None)
            code, resp = order_submit(goods_id, buy_count, to_phone, to_user, request)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ 订单支付页面 """
        try:
            sn = request.data.get('sn', None)
            code, resp = get_order_detail(request, sn)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

    def delete(self, request):
        """ 订单删除(逻辑删除) """
        try:
            sn = request.data.get('sn', None)
            code, resp = order_delete(request, sn)
            if code == RespCode.NO_CONTENT.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

    def put(self, request):
        """ 取消订单 """
        try:
            sn = request.data.get('sn', None)
            code, resp = order_cancel(request, sn)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

    def post(self, request):
        """ 立即支付 """
        try:
            sn = request.data.get('sn', None)
            code, resp = order_pay_submit(request, sn)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ 我的订单列表 """
        try:
            status = int(request.query_params.get('status'))
            code, resp = get_order_list(request, status)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')
