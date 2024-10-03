# 前台图书视图模块
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

from apps.collection.models import Collection
from apps.comment.models import Comment
from apps.common.models import Constant
from apps.item.models import Item
from apps.likerecord.models import Likerecord
from apps.scorerecord.models import Scorerecord
from apps.type.models import Type


# 图书详情
def detail(request):
    # 通过get请求获取图书id，是其他页面跳转到图书详情页面
    # 通过post请求获取图书id，是在图书详情页面中的评分请求中获取
    itemid = request.GET.get("itemid",request.POST.get("itemid"))
    # 查询当前图书
    item = Item.objects.get(id=itemid)
    data = {  # 返回参数
        "item": item,
    }
    page = request.POST.get("page", 1)  # 获取请求的页码，默认第一页
    # 查询评论，关联点赞记录，根据点赞数量降序查询
    sql = "select c.*, count(l.commentid) as likecount from comment c " \
          "left join likerecord l on c.id = l.commentid " \
          "where c.itemid = %s " \
          "group by c.id " \
          "order by likecount desc ,c.id desc" % itemid
    comments = Comment.objects.raw(sql)  # 查询
    paginator = Paginator(comments, Constant.pageSize)
    comments = paginator.page(page)  # 分页
    data["pageBean"] = comments
    data["page"] = page
    # 判断用户是否登录
    if Constant.session_user_isLogin in request.session \
            and request.session[Constant.session_user_isLogin]:
        # 获取session中的用户id
        userid = request.session[Constant.session_user_id]
        # 获取登录用户是否对当前图书进行评分
        scorerecord = Scorerecord.objects.filter(userid_id=userid,itemid_id=itemid)
        if len(scorerecord) > 0:
            data["scorerecord"] = scorerecord[0]
        # 获取登录用户是否对当前图书收藏
        collection = Collection.objects.filter(userid=userid, itemid=itemid)
        if len(collection) > 0:
            data["collection"] = collection[0]
        # 用户登录后，查询出用户对评论的点赞记录
        if comments and len(comments) > 0:
            for comment in comments:
                likerecord = Likerecord.objects.filter(userid_id=userid, commentid_id=comment.id)
                if likerecord and len(likerecord) > 0:
                    comment.likerecord = likerecord[0]
    return render(request,"item/detail.html",context=data)


