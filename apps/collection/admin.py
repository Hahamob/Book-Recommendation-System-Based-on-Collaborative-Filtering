# 后台admin收藏功能
from django.contrib import admin
from apps.collection.models import Collection
from apps.common.models import Constant
from apps.util.util import Util


# 后台admin的收藏功能类
@admin.register(Collection)  # 将collection类加入后台admin管理
class CollectionAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['showUsername', 'showItemname', 'createtime']
    # 列表展示字段添加链接（禁用，不允许修改）
    list_display_links = None
    # 列表页面的搜索框字段，模糊搜索：用户名、图书名称
    search_fields = ['userid__username', 'itemid__itemname']
    # 每页展示的条数
    list_per_page = Constant.pageSizeAdmin

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，用户外键的用户名
    def showUsername(self, obj):
        return obj.userid.username

    # 设置字段显示的标题
    showUsername.short_description = '用户名'

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，图书外键的图书名
    def showItemname(self, obj):
        return obj.itemid.itemname

    # 设置字段显示的标题
    showItemname.short_description = '图书名称'

    # 禁用添加按钮
    def has_add_permission(self, request):
        return False
