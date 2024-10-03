# 前台评分视图模块
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from apps.common.models import Constant
from apps.item.models import Item
from apps.scorerecord.models import Scorerecord
from apps.user.models import User
from apps.util.util import Util


# 添加/修改评分记录
def doScorerecord(request):
    post = request.POST
    score = post.get("score")  # 参数，评分
    itemid = post.get("itemid")  # 参数，图书主键
    user = User()
    # 当前登录用户主键
    user.id = request.session[Constant.session_user_id]
    # 查询是否有评分记录
    scorerecords = Scorerecord.objects.filter(itemid_id=itemid,userid_id=user.id)
    scorerecord = None
    # 如果已有评分记录，进行修改
    if len(scorerecords) > 0:  # 修改
        scorerecord = scorerecords[0]
        scorerecord.score = score
        scorerecord.save()
    else:  # 添加
        scorerecord = Scorerecord()
        item = Item()
        item.id = itemid
        scorerecord.itemid = item
        scorerecord.userid = user
        scorerecord.score = score
        scorerecord.createtime = Util().getCurrentTime()
        scorerecord.save()
    data = {
        "success":1,  # 1：操作成功
        "url":"reload"  # 重新加载请求的页面
    }
    return JsonResponse(data)


# 评分列表
def list(request):
    page = request.POST.get("page",1)  # 分页参数，默认是1
    userid = request.session[Constant.session_user_id]  # 用户主键
    # 查询当前登录用户的所有评分
    scorerecords = Scorerecord.objects.filter(userid_id=userid).order_by("-id")
    paginator = Paginator(scorerecords, Constant.pageSize)  # 分页
    scorerecords = paginator.page(page)
    data = {
        "pageBean":scorerecords,
        "page":page,
    }
    return render(request,"scorerecord/list.html",context=data)


# 删除评分记录
def delete(request):
    scorerecordid = request.POST.get("scorerecordid")  # 参数，评分记录主键
    userid = request.session.get(Constant.session_user_id)  # 当前登录用户主键
    Scorerecord.objects.filter(userid_id=userid,id=scorerecordid).delete()  # 删除
    data = {
        "success": 1,
        "url": "reload"
    }
    return JsonResponse(data)