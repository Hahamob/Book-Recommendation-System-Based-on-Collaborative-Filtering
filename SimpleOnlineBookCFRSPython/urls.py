# 路由配置文件，它的本质是URL模式以及要为该URL模式调用的视图函数之间的映射表

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SimpleOnlineBookCFRSPython import settings

urlpatterns = [
    path('',include('apps.common.urls')),  # 公共模块功能路由，前台登录、注册、注销、文件上传等
    path('',include('apps.index.urls')),  # 前台首页功能
    path('item/',include('apps.item.urls')),  # 前台图书功能
    path('user/',include('apps.user.urls')),  # 前台用户功能
    path('scorerecord/',include('apps.scorerecord.urls')),  # 前台评分功能
    path('comment/',include('apps.comment.urls')),  # 前台评论功能
    path('collection/',include('apps.collection.urls')),  # 前台收藏功能
    path('likerecord/',include('apps.likerecord.urls')),  # 前台点赞功能
    path('admin/', admin.site.urls),  # 后台管理员
]

# 设置图片路由访问规则: 访问 media 的接口会自动访问到本项目目录下的头像文件夹下的静态资源
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "在线图书推荐系统后台管理"  # 后台登录页面登录form框标题，后台页面头部标题
admin.site.site_title = "在线图书推荐系统后台管理"  # 后台网页的title
admin.site.index_title = "首页"  # 后台首页显示
