# 后台admin的前台用户管理功能
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from apps.common.models import Constant
from apps.user.models import User
from apps.util.util import Util


# 后台admin的前台用户管理功能类
@admin.register(User)  # 将user类加入后台admin管理
class UserAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['username', 'email', 'createtime']
    # 列表页面的搜索框字段
    search_fields = ['username']
    # 分页
    list_per_page = Constant.pageSizeAdmin
    # 编辑页面需要编辑的字段
    fields = ["username","email",'createtime']
    # 编辑页面的只读字段
    readonly_fields = ["username",'createtime']

    # 重写保存方法
    def save_model(self, request, obj, form, change):
        if not change:
            # 添加操作，目前管理员不支持添加用户操作
            messages.error(request, "操作失败！")
            messages.set_level(request, messages.ERROR)
        else:
            super().save_model(request, obj, form, change)

    # 禁用添加按钮
    def has_add_permission(self, request):
        return False








