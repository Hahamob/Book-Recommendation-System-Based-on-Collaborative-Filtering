"""
前台首页url
"""

from django.contrib import admin
from django.urls import path, include

from apps.index import views

urlpatterns = [
    path('',views.index),  # 前台首页url
    path('recommendCF',views.recommendCF),  # 个性化推荐url
    path('recommendHot',views.recommendHot),  # 热点推荐url
]
