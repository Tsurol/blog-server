import random

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction

from authentication.serializers import UserProfileSerializer
from blogsite.models import Blog, Tag, LoveRelated, Comment, AdviceUpload
from blogsite.serializers import BlogSerializer, TagSerializer, BlogDetailSerializer, BlogCommentSerializer
from utils.email_service import start_send_mail
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
        fields = ('id', 'title', 'desc', 'created_at', 'bkc', 'user', 'comment_count', 'love_count', 'is_top', 'img')
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
    if blog_id and not comment_id:  # 点赞博客
        blog_qs = Blog.objects.filter(id=blog_id, is_valid=True).first()
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        love_qs = blog_qs.love.filter(user=user).first()
        if love_qs:
            if love_qs.is_valid is True:
                love_qs.is_valid = False
                love_qs.save()
                return RespCode.CREATED.value, {}
            love_qs.is_valid = True
            love_qs.save()
        else:
            blog_qs.love.create(user=user)
        # content = ContentType.objects.filter(app_label='blogsite', model='blog').first()
        # blog_love_count = LoveRelated.objects.filter(content_type=content, object_id=blog_id).count()
        return RespCode.CREATED.value, {}

    if comment_id and not blog_id:  # 点赞评论
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
    resp = {
        'comment_count': len(comment_qs) if comment_qs else 0
    }
    return RespCode.OK.value, resp


def get_blog_detail(blog_id):
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        fields = ('id', 'title', 'desc', 'created_at', 'user', 'content',
                  'comment_count', 'love_count', 'img', 'is_origin', 'category')
        resp = {
            'data': BlogDetailSerializer(blog_qs, fields=fields).data,
        }
        return RespCode.OK.value, resp
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_blog_comment(blog_id, is_reorder):
    comment_all_qs = Comment.objects.filter(is_valid=True, blog=blog_id, reply_id__isnull=True).all()
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        comment_qs = Comment.objects.filter(is_valid=True, blog=blog_qs, reply_id__isnull=True).order_by(
            '-created_at').all()
        if not comment_qs:
            return RespCode.NOT_FOUND.value, '暂无评论'
        fields = (
            'id', 'content', 'reply', 'user', 'created_at', 'is_top', 'profile', 'temporary_nickname',
            'temporary_avatar', 'love_count', 'blog')
        resp = {
            'data': BlogCommentSerializer(comment_qs, many=True, fields=fields).data,
            'comment_count': len(comment_all_qs) if comment_all_qs else 0
        }
        return RespCode.OK.value, resp
    if is_reorder == str(Constants.ORDER_BY_CREATED.value):
        comment_all_blog = Comment.objects.filter(is_valid=True, reply_id__isnull=True).all()
        # 最新评论，按时间排序
        comment_all_blog = comment_all_blog.order_by(
            '-created_at')[:5]
        if not comment_all_blog:
            return RespCode.NOT_FOUND.value, '暂无评论'
        fields = (
            'id', 'content', 'reply', 'user', 'created_at', 'is_top', 'profile', 'temporary_nickname',
            'temporary_avatar', 'love_count', 'blog', 'blog_title')
        resp = {
            'data': BlogCommentSerializer(comment_all_blog, many=True, fields=fields).data,
        }
        return RespCode.OK.value, resp


def post_blog_comment(request, temporary, blog_id, reply_id, content):
    # user = current_user(request)
    # if not user:
    #     # 临时用户(仅可以评论)
    #     if blog_id:
    #         if reply_id:
    #             # 是一条回复,匿名用户的评论和回复
    #             Comment.objects.create(content=content, reply_id=reply_id,
    #                                    blog_id=blog_id, temporary=temporary)
    #             return RespCode.CREATED.value, {}
    #         # 是一条评论
    #         Comment.objects.create(content=content, blog_id=blog_id, temporary=temporary)
    #         return RespCode.CREATED.value, {}
    #     return RespCode.BAD_REQUEST.value, '请求参数错误'
    # 正式用户,可以评论
    if blog_id:
        if reply_id:
            if not all([temporary, content]):
                return RespCode.BAD_REQUEST.value, '请填写您的昵称和评论内容'
            # 是一条回复,匿名用户的评论和回复
            Comment.objects.create(content=content, reply_id=reply_id,
                                   blog_id=blog_id, temporary=temporary)
            return RespCode.CREATED.value, {}
        # 是一条评论
        if not all([temporary, content]):
            return RespCode.BAD_REQUEST.value, '请填写您的昵称和评论内容'
        Comment.objects.create(content=content, blog_id=blog_id, temporary=temporary)
        return RespCode.CREATED.value, {}
    return RespCode.BAD_REQUEST.value, '缺失请求参数'

    # if blog_id:
    #     if reply_id:
    #         Comment.objects.create(content=content, reply_id=reply_id, blog_id=blog_id, user=user)
    #         return RespCode.CREATED.value, {}
    #     Comment.objects.create(content=content, blog_id=blog_id, user=user)
    #     return RespCode.CREATED.value, {}
    # return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_comment_reply(blog_id):
    if blog_id:
        blog_qs = Blog.objects.get(pk=blog_id, is_valid=True)
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        reply_qs = Comment.objects.filter(is_valid=True, blog=blog_qs, reply_id__isnull=False).all()
        if not reply_qs:
            return RespCode.NOT_FOUND.value, '暂无评论'
        fields = (
            'id', 'content', 'reply', 'user', 'format_created_at', 'is_top', 'profile', 'temporary_nickname',
            'temporary_avatar')
        resp = {
            'data': BlogCommentSerializer(reply_qs, many=True, fields=fields).data,
        }
        return RespCode.OK.value, resp
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_blog_author(blog_id):
    if blog_id:
        blog_qs = Blog.objects.filter(is_valid=True, id=blog_id).first()
        if not blog_qs:
            return RespCode.NOT_FOUND.value, '该博客不存在'
        author = blog_qs.user
        if not author.profile.is_valid:
            return RespCode.BAD_REQUEST.value, '用户个人信息已被删除'
        fields = ('user', 'username', 'nickname', 'avatar', 'sex', 'age', 'coins', 'words', 'blog')
        user_profile_data = UserProfileSerializer(author.profile, fields=fields).data
        return RespCode.OK.value, user_profile_data
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def get_random_blog():
    random_blog = random.sample(list(Blog.objects.filter(is_valid=True).all()), 5)
    resp = {
        'data': BlogSerializer(random_blog, many=True).data,
    }
    return RespCode.OK.value, resp


def post_advice(name, mobile, advice):
    # 需要三个参数都存在
    if all([name, mobile, advice]):
        AdviceUpload.objects.create(name=name, mobile=mobile, advice=advice)
        msg = """
        客户名: {name} \n
        手机号: {mobile} \n
        需求描述: {advice} \n
        \n\n\n\n
        copyright © xxxxxx｜周梓凌的个人网站
        """.format(name=name, mobile=mobile, advice=advice)
        start_send_mail(msg)
        return RespCode.CREATED.value, {}
    return RespCode.BAD_REQUEST.value, '请求参数错误'


def create_blog(request, title, desc, category, origin, content, file, tags):
    user = current_user(request)
    if not user:
        return RespCode.BAD_REQUEST.value, '该账号不存在'
    if not user.profile.is_valid:
        return RespCode.BAD_REQUEST.value, '用户个人信息已被删除'
    if all([title, desc, category, origin, content, tags]):
        if origin == 'true':
            origin = True
        else:
            origin = False
        with transaction.atomic():
            if not file:
                blog_obj = Blog.objects.create(user=user, title=title, desc=desc, category_id=category,
                                               is_origin=origin,
                                               content=content, is_valid=False)
            else:
                blog_obj = Blog.objects.create(user=user, title=title, img=file, desc=desc, category_id=category,
                                               is_origin=origin,
                                               content=content, is_valid=False)
            tags_str = str(tags[0])
            tags_ls = tags_str.split(',')
            for tag in tags_ls:
                tag_obj = Tag.objects.filter(name=tag).first()
                tag_obj.blog.add(blog_obj)
            return RespCode.CREATED.value, {}
    return RespCode.BAD_REQUEST.value, '请求参数缺失'
