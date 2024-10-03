# 后台admin评论功能
from django.contrib import admin
from apps.comment.models import Comment
from apps.common.models import Constant
from apps.util.util import Util


# 后台admin的评论功能类
@admin.register(Comment)  # 将comment类加入后台admin管理
class CommentAdmin(admin.ModelAdmin):
    # 列表展示字段
    list_display = ['showUsername', 'showItemname','contentShort','createtime']
    # 列表展示字段添加链接（跳转到详情或者修改页面）
    list_display_links = ['showUsername', 'showItemname','contentShort',]
    # 列表页面的搜索框字段，模糊搜索：用户名、图书名称
    search_fields = ['userid__username','itemid__itemname']
    # 每页展示的条数
    list_per_page = Constant.pageSizeAdmin
    # 编辑页面需要编辑的字段
    fields = ["userid","itemid","content",'createtime']
    # 编辑页面的只读字段
    readonly_fields = ["userid","itemid","content",'createtime']

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，用户外键的用户名
    def showUsername(self,obj):
        return obj.userid.username

    # 设置字段显示的标题
    showUsername.short_description = '用户名'

    # 列表展示页面，有些字段需要格式化或者显示外键的某些属性，图书外键的图书名
    def showItemname(self,obj):
        return obj.itemid.itemname

    # 设置字段显示的标题
    showItemname.short_description = '图书名称'

    # 禁用添加按钮
    def has_add_permission(self, request):
        return False



