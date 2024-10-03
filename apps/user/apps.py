# 定义应用程序
from django.apps import AppConfig


class AppsConfig(AppConfig):
    name = 'apps.user'
    verbose_name = "1、前台用户管理"  # 后台admin首页显现的导航栏，1主要是为了排序
