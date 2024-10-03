"""
前台评分记录功能url
"""

from django.contrib import admin
from django.urls import path, include

from apps.scorerecord import views

urlpatterns = [
    path('doScorerecord',views.doScorerecord),  # 添加/修改评分记录
    path('list',views.list),  # 评分记录列表
    path('delete',views.delete),  # 删除
]
