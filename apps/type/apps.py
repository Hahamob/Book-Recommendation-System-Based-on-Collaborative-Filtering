# 定义应用程序
from django.apps import AppConfig


class AppsConfig(AppConfig):
    name = 'apps.type'
    verbose_name = "2、图书类型管理"  # 后台admin首页显现的导航栏，2主要是为了排序
