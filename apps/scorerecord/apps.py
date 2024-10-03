# 定义应用程序
from django.apps import AppConfig


class AppsConfig(AppConfig):
    name = 'apps.scorerecord'
    verbose_name = "4、评分记录管理"  # 后台admin首页显现的导航栏，4主要是为了排序
