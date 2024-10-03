"""
公共模块的url
"""

from django.contrib import admin
from django.urls import path, include

from apps.common import views

urlpatterns = [
    path('login',views.login,name="login"),  # 跳转到登录页面，这里设置name，为了在模板文件中直接写name，就能找到这个路由
    path('register',views.register,name="register"),  # 跳转到注册页面，这里设置name，为了在模板文件中直接写name，就能找到这个路由
    path('doLogin',views.doLogin),  # 登录
    path('doRegister',views.doRegister),  # 注册
    path('logout',views.logout),  # 注销
]
