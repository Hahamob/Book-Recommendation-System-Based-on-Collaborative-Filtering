# 后台admin图书管理功能
from django.contrib import admin
from django.utils.safestring import mark_safe
from apps.common.models import Constant
from apps.item.models import Item
from apps.util.util import Util


# 后台admin的图书管理功能类
@admin.register(Item)  # 将item类加入后台admin管理
class ItemAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['itemname', 'showTypename','createtime']
    # 列表页面的搜索框字段
    search_fields = ['itemname']
    # 每页展示的条数
    list_per_page = Constant.pageSizeAdmin
    # 编辑页面需要编辑的字段
    fields = ["itemname","typeid","showImage","image","content"]
    # 编辑页面的只读字段
    readonly_fields = ["showImage",]
    # 列表页面的过滤器过滤字段
    list_filter = ('typeid__typename',)

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，类型外键的类型名
    def showTypename(self,obj):
        return obj.typeid.typename

    # 设置字段显示的标题
    showTypename.short_description = '图书类型'

    # 编辑页面，有些字段需要格式化或者显示外键的某些属性，图书封面
    def showImage(self,obj):
        try:
            image = mark_safe('<img src="%s" width="80px" />' % (obj.image.url,))
        except Exception as e:
            image = ''
        return image

    # 设置字段显示的标题
    showImage.short_description = "封面展示"

    # 重写保存方法
    def save_model(self, request, obj, form, change):
        if not change:
            # 添加
            obj.createtime = Util().getCurrentTime()  # 添加时间
        super().save_model(request, obj, form, change)
