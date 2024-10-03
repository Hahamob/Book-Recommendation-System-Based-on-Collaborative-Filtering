# 后台admin图书类型功能
from django.contrib import admin
from apps.common.models import Constant
from apps.type.models import Type


# 后台admin的图书类型功能类
@admin.register(Type)  # 将type类加入后台admin管理
class TypeAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['typename']
    # 列表页面查询字段
    search_fields = ['typename']
    # 分页
    list_per_page = Constant.pageSizeAdmin
    # 编辑页面需要编辑的字段
    fields = ["typename"]
