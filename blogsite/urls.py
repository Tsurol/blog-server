from django.urls import re_path
from blogsite import views

urlpatterns = [
    re_path("blogsite/list/", views.BlogListView.as_view()),
    re_path("tag/list/", views.TagListView.as_view()),
    re_path("blogsite/love/", views.BlogLoveView.as_view()),
]
