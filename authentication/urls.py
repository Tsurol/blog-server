from django.urls import re_path, path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)
from authentication import views

urlpatterns = [
    re_path(r'^email/code/', views.SendEmailCodeView.as_view()),
    re_path(r'^email/register/', views.EmailRegisterView.as_view()),
    re_path(r'^email/login/', views.LoginByEmailView.as_view()),
    re_path(r'^code/login/', views.LoginByEmailCodeView.as_view()),
    re_path(r'^email/reset/', views.ResetPasswordByEmailView.as_view()),

    re_path(r'^user/info/', views.UserInfoView.as_view()),

    re_path(r'^user/list/', views.UserListView.as_view()),
    re_path('^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
