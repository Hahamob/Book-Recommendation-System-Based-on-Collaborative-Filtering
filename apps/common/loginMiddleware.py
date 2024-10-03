# 登录权限验证中间件
# 验证用户、管理员是否登录，有些功能需要登录后才能操作
from django.http import HttpResponseRedirect
from rpvputil.common.abstractmiddleware import AbstractMiddleware

from SimpleOnlineBookCFRSPython import settings
from apps.common.models import Constant


# 定义登录权限验证中间件
class LoginMiddleware(AbstractMiddleware):

    # 在执行具体的请求之前，进行验证
    def process_request(self, request):
        path = request.path  # 请求的url
        # 设置不需要登录就能够访问的url
        noAuthPath = ",/,/login,/doLogin,/register,/doRegister,/logout" \
                     ",/item/detail,/recommendHot,"
        # 后台管理员操作和上传的资源不需要验证
        if path.startswith(settings.MEDIA_URL) or path.startswith("/admin/"):
            pass
        else:
            path = "," + path + ","
            if path not in noAuthPath:
                # 判断session中是否有前台登录用户数据
                if request.session.get(Constant.session_user_isLogin, None):
                    pass
                else:
                    return HttpResponseRedirect('/login')  # 返回登录页面

