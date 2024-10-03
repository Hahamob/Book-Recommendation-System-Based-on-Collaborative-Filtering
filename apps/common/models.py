# 公共模块常量
from django.db import models



# 定义常量类
class Constant(object):

    pageSize = 12  # 前台分页条数

    pageSizeAdmin = 10  # 后台分页条数

    session_user_isLogin = "session_user_isLogin"  # session中保存的前台登录用户的判断键值

    session_user_id = "session_user_id"  # session中保存的前台登录用户的主键键值

    session_user_username = "session_user_username"  # session中保存的前台登录用户的用户名键值



