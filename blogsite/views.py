from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from blogsite.bussiness import get_blog_list, get_tag_list
from utils.enums import RespCode
from utils.response import reformat_resp


class BlogListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            is_hot = request.query_params.get('is_hot', None)
            is_top = request.query_params.get('is_top', None)
            code, resp = get_blog_list(request, is_hot, is_top)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class TagListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            code, resp = get_tag_list()
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')
