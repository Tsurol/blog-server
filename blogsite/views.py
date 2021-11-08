from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from blogsite.bussiness import get_blog_list, get_tag_list, love_blog, get_blog_by_tag, comment_count
from utils.enums import RespCode
from utils.response import reformat_resp


class BlogListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            search = request.query_params.get('search', None)
            is_hot = request.query_params.get('is_hot', None)
            is_top = request.query_params.get('is_top', None)
            code, resp = get_blog_list(request, is_hot, is_top, search)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class SearchBlogByTagView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            tag_id = request.data.get('tag_id', None)
            code, resp = get_blog_by_tag(request, tag_id)
            if code == RespCode.CREATED.value:
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


class BlogLoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            blog_id = int(request.data.get('blog_id', None))
            code, resp = love_blog(request, blog_id)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class CommentCountView(APIView):
    """ 统计所有博客的评论数量 """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            code, resp = comment_count()
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')