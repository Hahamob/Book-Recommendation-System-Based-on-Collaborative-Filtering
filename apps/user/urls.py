"""
前台用户url
"""

from django.contrib import admin
from django.urls import path, include

from apps.user import views

urlpatterns = [
    path('edit',views.edit),  # 跳转到用户信息编辑页面
    path('doEdit',views.doEdit),  # 更新用户信息
    path('password',views.password),  # 跳转到修改密码页面
    path('doPassword',views.doPassword),  # 更新用户密码
]
