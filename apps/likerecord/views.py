# 前台点赞视图模块
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from apps.likerecord.models import Likerecord
from apps.common.models import Constant
from apps.user.models import User
from apps.util.util import Util


# 添加/取消点赞
def save(request):
    post = request.POST  # 获取请求方式
    commentid = post.get("commentid")  # 获取请求参数评论主键
    itemid = post.get("itemid")  # 获取请求参数图书主键
    userid = request.session[Constant.session_user_id]  # 从session中获取当前登录用户的id
    likerecord = Likerecord.objects.filter(commentid=commentid, itemid=itemid, userid=userid)  # 查找点赞记录
    if len(likerecord) > 0:
        likerecord.delete()  # 如果存在点赞记录，那么删除
    else:
        likerecord = Likerecord()
        likerecord.userid_id = userid
        likerecord.commentid_id = commentid
        likerecord.itemid_id = itemid
        likerecord.createtime = Util().getCurrentTime()
        likerecord.save()  # 添加点赞记录
    data = {  # 返回参数
        "success":1,  # 1：操作成功
        "url":"reload"  # 重新加载请求的页面
    }
    return JsonResponse(data)


# 点赞列表
def list(request):
    page = request.POST.get("page", 1)  # 获取请求的页码，如果不存在就请求第一页
    userid = request.session[Constant.session_user_id]
    likerecords = Likerecord.objects.filter(userid_id=userid).order_by("-id")  # 查找当前用户的点赞记录，id降序
    paginator = Paginator(likerecords, Constant.pageSize)
    likerecords = paginator.page(page)  # 分页
    data = {  # 返回参数
        "pageBean": likerecords,
        "page": page,
    }
    return render(request, "likerecord/list.html", context=data)
