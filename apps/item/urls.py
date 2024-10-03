"""
图书功能前台url
"""

from django.contrib import admin
from django.urls import path, include

from apps.item import views

urlpatterns = [
    path('detail',views.detail),  # 图书详情
]
