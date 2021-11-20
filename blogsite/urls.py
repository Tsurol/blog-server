from django.urls import re_path
from blogsite import views

urlpatterns = [
    re_path("blogsite/list/", views.BlogListView.as_view()),
    re_path("blogsite/detail/", views.BlogDetailView.as_view()),
    re_path("tag/list/", views.TagListView.as_view()),
    re_path("blogsite/love/", views.LoveView.as_view()),
    re_path("tag/blog/list/", views.SearchBlogByTagView.as_view()),
    re_path("comment/count/", views.CommentCountView.as_view()),
    re_path("blogsite/comment/", views.BlogCommentView.as_view()),
    re_path("comment/reply/", views.CommentReplyView.as_view()),
    re_path("author/info/", views.AuthorInfoView.as_view()),
    re_path("random/blog/", views.RandomBlogView.as_view()),
    re_path("advice/", views.AdviceView.as_view()),
    re_path("create/blog/", views.CreateBlogView.as_view()),
]
