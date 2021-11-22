import os

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from blog import settings
from blog.settings import MEDIA_ROOT
from blogsite.bussiness import get_blog_list, get_tag_list, get_blog_by_tag, comment_count, get_blog_detail, \
    get_blog_comment, love_obj, post_blog_comment, get_blog_author, get_comment_reply, get_random_blog, post_advice, \
    create_blog
from utils.enums import RespCode
from utils.response import reformat_resp


class BlogListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            search = request.query_params.get('search', None)
            is_hot = request.query_params.get('is_hot', None)
            is_top = request.query_params.get('is_top', None)
            current_page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('limit', 8))
            code, resp = get_blog_list(request, is_hot, is_top, search, current_page, page_size)
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


class BlogDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            blog_id = request.query_params.get('blog_id', None)
            code, resp = get_blog_detail(blog_id)
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
            blog_id = request.query_params.get('blog_id', None)
            code, resp = get_tag_list(blog_id)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class LoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            blog_id = request.data.get('blog_id', None)
            comment_id = request.data.get('comment_id', None)
            code, resp = love_obj(request, blog_id, comment_id)
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


class BlogCommentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """ 获取评论列表 """
        try:
            blog_id = request.query_params.get('blog_id', None)
            is_reorder = request.query_params.get('order', None)
            # order==1:按创建时间排序,order==2:按is_top排序
            code, resp = get_blog_comment(blog_id, is_reorder)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')

    def post(self, request):
        """ 发布评论(包括回复) """
        try:
            content = request.data.get('content', None)
            blog_id = request.data.get('blog_id', None)
            reply_id = request.data.get('reply_id', None)
            # 临时用户的名称(前端传入)
            temporary = request.data.get('temporary', None)
            code, resp = post_blog_comment(request, temporary, blog_id, reply_id, content)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class CommentReplyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """ 获取评论的回复列表 """
        try:
            blog_id = request.query_params.get('blog_id', None)
            code, resp = get_comment_reply(blog_id)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class AuthorInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """ 获取博客的作者信息 """
        try:
            blog_id = request.query_params.get('blog_id', None)
            code, resp = get_blog_author(blog_id)
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class RandomBlogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """ 获取相关博客信息"""
        try:
            code, resp = get_random_blog()
            if code == RespCode.OK.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class AdviceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            name = request.data.get('name', '')
            mobile = request.data.get('mobile', '')
            advice = request.data.get('advice', '')
            code, resp = post_advice(name, mobile, advice)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')


class CreateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            title = request.data.get('title', None)
            desc = request.data.get('desc', None)
            category = request.data.get('category', None)
            origin = request.data.get('origin', None)
            # 获取前端传递的数组
            tags = request.data.getlist('tags')
            content = request.data.get('content', None)
            file = request.FILES.get('file', None)
            code, resp = create_blog(request, title, desc, category, origin, content, file, tags)
            if code == RespCode.CREATED.value:
                return reformat_resp(code, resp, 'Succeed')
            else:
                return reformat_resp(code, {}, resp)
        except Exception as e:
            print(e)
        return reformat_resp(RespCode.INTERNAL_SERVER_ERROR.value, {}, 'Internal Server Error')
