from django.core.paginator import Paginator
from django.db import transaction

from blogsite.models import Blog, Tag, LoveRelated, Comment
from blogsite.serializers import BlogSerializer, TagSerializer, BlogDetailSerializer, BlogCommentSerializer
from utils.enums import RespCode, Constants
from utils.pagination import MyPagination
from utils.verify import current_user


def get_blog_list(request, is_hot, is_top, search, current_page, page_size):
    bolg_qs = Blog.objects.filter(is_valid=True).all().order_by('-is_top')
    if is_hot:
        bolg_qs = Blog.objects.filter(is_valid=True, is_hot=True).all().order_by('-updated_at')
    if is_top:
        bolg_qs = Blog.objects.filter(is_valid=True, is_top=True).all().order_by('-updated_at')
    if search:
        bolg_qs = Blog.objects.filter(is_valid=True, desc__icontains=search).all().order_by('-updated_at')
    if not bolg_qs:
        return RespCode.NOT_FOUND.value, '查找的博客不存在'
    paginator = Paginator(bolg_qs, page_size)
    page_data = paginator.page(current_page)
    fields = ('id', 'title', 'desc', 'created_at', 'bkc', 'user', 'comment_count', 'love_count', 'is_top', 'img')
    resp = {
        'data': BlogSerializer(page_data, many=True, fields=fields).data,
    }
    return RespCode.OK.value, resp


def get_blog_by_tag(request, tag_id):
    if tag_id:
        tag_qs = Tag.objects.get(id=tag_id)
        if not tag_qs:
            return RespCode.NOT_FOUND.value, '标签不存在'
        blog_qs = tag_qs.blog.all()
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该标签对应的博客不存在'
        page_obj = MyPagination()
        page_res = page_obj.paginate_queryset(queryset=blog_qs, request=request)
        fields = ('id', 'title', 'desc', 'created_at', 'bkc', 'user', 'comment_count', 'love_count', 'is_top')
        resp = {
            'data': BlogSerializer(page_res, many=True, fields=fields).data
        }
        return RespCode.CREATED.value, resp
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_tag_list(blog_id):
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        tag_qs = Tag.objects.filter(is_valid=True, blog=blog_qs)
    else:
        tag_qs = Tag.objects.filter(is_valid=True).all()
    if not tag_qs:
        return RespCode.NOT_FOUND.value, '查找的标签不存在'
    fields = ('id', 'name', 'bkc', 'blog')
    resp = {
        'data': TagSerializer(tag_qs, many=True, fields=fields).data
    }
    return RespCode.OK.value, resp


def love_obj(request, blog_id, comment_id):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    if blog_id and not comment_id:
        blog_qs = Blog.objects.filter(id=blog_id, is_valid=True).first()
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        love_qs = blog_qs.love.first()

        if love_qs:
            if love_qs.is_valid is True:
                love_qs.is_valid = False
                love_qs.save()
                return RespCode.CREATED.value, {}
            love_qs.is_valid = True
            love_qs.save()
        else:
            blog_qs.love.create(user=user)
        return RespCode.CREATED.value, {}

    if comment_id and not blog_id:
        comment_qs = Comment.objects.filter(id=comment_id, is_valid=True).first()
        if not comment_qs:
            return RespCode.NOT_FOUND.value, '该评论不存在'
        love_qs = comment_qs.love.first()
        if love_qs:
            if love_qs.is_valid is True:
                love_qs.is_valid = False
                love_qs.save()
                return RespCode.CREATED.value, {}
            love_qs.is_valid = True
            love_qs.save()
        else:
            comment_qs.love.create(user=user)
        return RespCode.CREATED.value, {}

    return RespCode.BAD_REQUEST.value, '请求参数错误'


def comment_count():
    comment_qs = Comment.objects.filter(is_valid=True).only('id').all()
    if not comment_qs:
        return RespCode.OK.value, {
            'comment_count': 0
        }
    resp = {
        'comment_count': len(comment_qs)
    }
    return RespCode.OK.value, resp


def get_blog_detail(blog_id):
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        fields = ('id', 'title', 'desc', 'created_at', 'user', 'content', 'comment_count', 'love_count', 'img')
        resp = {
            'data': BlogDetailSerializer(blog_qs, fields=fields).data,
        }
        return RespCode.OK.value, resp
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_blog_comment(blog_id, is_reorder):
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        comment_qs = Comment.objects.filter(is_valid=True, blog=blog_qs).all()
        if is_reorder == str(Constants.ORDER_BY_CREATED.value):
            # 最新评论，按时间排序
            comment_qs = Comment.objects.filter(is_valid=True, blog=blog_qs, reply_id=None).all().order_by('-created_at')
        elif is_reorder == str(Constants.ORDER_BY_IS_TOP.value):
            # 按is_top排序
            comment_qs = Comment.objects.filter(is_valid=True, blog=blog_qs, reply_id=None).all().order_by('-is_top')
        if not comment_qs:
            return RespCode.NOT_FOUND.value, '暂无评论'
        fields = ('id', 'content', 'reply', 'user', 'created_at', 'is_top')
        resp = {
            'data': BlogCommentSerializer(comment_qs, many=True, fields=fields).data,
        }
        return RespCode.OK.value, resp
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def post_blog_comment(request, temporary, blog_id, reply_id, content):
    user = current_user(request)
    if not user:
        # 临时用户(仅可以评论)
        if blog_id:
            if reply_id:
                # 是一条回复,匿名用户的评论和回复
                Comment.objects.create(content=content, reply_id=reply_id,
                                       blog_id=blog_id, temporary=temporary)
                return RespCode.CREATED.value, {}
            # 是一条评论
            Comment.objects.create(content=content, blog_id=blog_id, temporary=temporary)
            return RespCode.CREATED.value, {}
        return RespCode.BAD_REQUEST.value, '请求参数错误'
    # 正式用户,可以评论
    if blog_id:
        if reply_id:
            Comment.objects.create(content=content, reply_id=reply_id, blog_id=blog_id, user=user)
            return RespCode.CREATED.value, {}
        Comment.objects.create(content=content, blog_id=blog_id, user=user)
        return RespCode.CREATED.value, {}
    return RespCode.BAD_REQUEST.value, '请求参数错误'
