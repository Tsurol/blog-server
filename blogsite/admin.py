from django.contrib import admin
from blogsite import models

admin.AdminSite.site_header = '周梓凌的个人网站'
admin.AdminSite.site_title = '周梓凌的个人网站'

admin.site.register(models.Blog)
admin.site.register(models.Comment)
