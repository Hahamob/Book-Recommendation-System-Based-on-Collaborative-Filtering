"""
点赞功能前台url
"""

from django.contrib import admin
from django.urls import path, include

from apps.likerecord import views

urlpatterns = [
    path('save',views.save),  # 添加/取消点赞
    path('list',views.list),  # 点赞列表
]
