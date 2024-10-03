# 公共视图模块
import json
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect

from SimpleOnlineBookCFRSPython import settings
from apps.common.models import Constant
from apps.user.models import User
from apps.util.util import Util


# 跳转到登录页面
def login(request):
    return render(request, "common/login.html")


# 登录
def doLogin(request):
    post = request.POST
    username = post.get('username')  # 参数，用户名
    password = post.get('password')  # 参数，密码
    users = User.objects.filter(username=username, password=password)  # 查询用户
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    url = ""  # 操作结果返回的url
    if len(users) != 0:
        success = 1  # 操作成功
        sessionUser = users[0]  # 当前登录用户对象
        # 将登录信息保存到session中
        request.session[Constant.session_user_isLogin] = True  # 用户是否登录
        request.session[Constant.session_user_id] = sessionUser.id  # 用户id
        request.session[Constant.session_user_username] = sessionUser.username  # 用户名
        # 登录成功跳转到首页
        url = "/"
    else:
        message = "用户名或者密码错误！"
    return JsonResponse({"success": success, "message": message, "url": url})


# 跳转到注册页面
def register(request):
    return render(request, "common/register.html")


# 注册
def doRegister(request):
    post = request.POST
    username = post.get('username')  # 参数，用户名
    password = post.get('password')  # 参数，密码
    users = User.objects.filter(username=username)  # 查询用户名是否已经存在
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    url = ""  # 操作结果返回的url
    if len(users) != 0:
        success = -1
        message = "操作失败！用户名已存在！"
    else:
        user = User()  # 创建用户实体类
        user.username = username  # 设置用户名
        user.password = password  # 设置密码
        user.createtime = Util().getCurrentTime()  # 注册时间
        user.save()  # 保存注册的用户
        success = 1
        url = "/login"  # 跳转到用户登录页面
    return JsonResponse({"success": success, "message": message, "url": url})


# 注销
def logout(request):
    if not request.session.get(Constant.session_user_isLogin, None):
        # 如果没有登录，不进行注销操作
        return redirect("/")
    del request.session[Constant.session_user_isLogin]  # 删除session会话中的 用户是否登录变量
    del request.session[Constant.session_user_id]  # 删除session会话中的 用户id
    del request.session[Constant.session_user_username]  # 删除session会话中的 用户名
    return redirect('/')


