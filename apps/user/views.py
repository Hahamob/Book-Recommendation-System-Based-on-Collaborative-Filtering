# 前台用户视图模块
from django.http import JsonResponse
from django.shortcuts import render, redirect
from apps.common.models import Constant
from apps.user.models import User


# 跳转到用户编辑页面
def edit(request):
    # 查询用户信息
    user = User.objects.get(id=request.session[Constant.session_user_id])
    data = {
        "user": user,
    }
    return render(request, "user/edit.html", context=data)


# 保存用户修改的数据
def doEdit(request):
    post = request.POST
    email = post.get("email")  # 参数，邮箱
    # 查询并更新
    success = User.objects.filter(id=request.session[Constant.session_user_id])\
        .update(email=email)
    data = {
        "success":success,
        "url":"reload",  # 刷新页面
    }
    return JsonResponse(data)


# 跳转到修改密码页面
def password(request):
    return render(request,"user/password.html")


# 修改密码
def doPassword(request):
    post = request.POST
    oldPassword = post.get("oldPassword")  # 参数，原密码
    password = post.get("password")  # 参数，新密码
    # 获取session中用户主键并查询
    user = User.objects.get(id=request.session[Constant.session_user_id])
    success = 0  # 操作是否成功标记，小于或者等于0：操作失败，大于0：操作成功
    message = ""  # 操作结果提示信息
    url = ""  # 操作结果返回的url
    # 判断原密码是否正确
    if user.password == oldPassword:
        # 更新
        success = User.objects.filter(id=user.id).update(password=password)
        if success > 0:
            url = "/login"
            request.session.flush()
    else:
        message = "原密码不正确！"
    data = {
        "success":success,
        "url":url,
        "message":message,
    }
    return JsonResponse(data)






