"""
评论功能前台url
"""

from django.contrib import admin
from django.urls import path, include

from apps.comment import views

urlpatterns = [
    path('doComment',views.doComment),  # 添加评论
    path('list',views.list),  # 评论列表
    path('detail',views.detail),  # 评论详情
    path('edit',views.edit),  # 评论编辑
    path('doEdit',views.doEdit),  # 更新评论
    path('delete',views.delete),  # 评论删除
]
