# 前台收藏视图模块
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from apps.collection.models import Collection
from apps.common.models import Constant
from apps.item.models import Item
from apps.user.models import User
from apps.util.util import Util


# 添加/取消收藏
def doCollection(request):
    post = request.POST  # 获取请求方式
    itemid = post.get("itemid")  # 获取请求参数图书主键
    userid = request.session[Constant.session_user_id]  # 从session中获取当前登录用户的id
    collection = Collection.objects.filter(itemid=itemid, userid=userid)  # 查找收藏记录
    if len(collection) > 0:
        collection.delete()  # 如果存在收藏记录，那么删除
    else:  # 添加收藏
        collection = Collection()
        collection.userid_id = userid
        collection.itemid_id = itemid
        collection.createtime = Util().getCurrentTime()
        collection.save()  # 添加收藏记录
    data = {  # 返回参数
        "success": 1,  # 1：操作成功
        "url": "reload"  # 重新加载请求的页面
    }
    return JsonResponse(data)


# 收藏列表
def list(request):
    page = request.POST.get("page", 1)  # 获取请求的页码，如果不存在就请求第一页
    userid = request.session[Constant.session_user_id] # 从session中获取当前登录用户的id
    records = Collection.objects.filter(userid_id=userid).order_by("-id")  # 查找当前用户的收藏记录，id降序
    paginator = Paginator(records, Constant.pageSize)
    records = paginator.page(page)  # 分页
    data = {  # 返回参数
        "pageBean": records,
        "page": page,
    }
    return render(request, "collection/list.html", context=data)
