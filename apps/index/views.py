# 前台首页视图模块
import operator
from math import sqrt

from django.core.paginator import Paginator
from django.shortcuts import render
from apps.common.models import Constant
from apps.item.models import Item
from apps.scorerecord.models import Scorerecord
from apps.type.models import Type


# 前台首页
def index(request):
    page = request.POST.get("page", 1)  # 分页参数，请求第几页，默认第一页
    itemname = request.POST.get("itemname", "")  # 参数，搜索图书名称
    typeid = request.POST.get("typeid", "")  # 参数，图书类型主键
    types = Type.objects.all()  # 查询所有图书类型
    items = None  # 定义返回的图书集合
    if itemname == "":
        if typeid == "":
            items = Item.objects.all().order_by("-id")  # 获取所有图书，id降序排列
        else:
            typeid = int(typeid)
            items = Item.objects.filter(typeid_id=typeid).order_by("-id")  # 带参数，图书类型查询
    else:
        if typeid == "":
            items = Item.objects.filter(itemname__icontains=itemname).order_by("-id")  # 带参数，图书名称模糊查询
        else:
            typeid = int(typeid)
            # 带参数，图书类型、图书名称查询
            items = Item.objects.filter(itemname__icontains=itemname, typeid_id=typeid).order_by("-id")
    paginator = Paginator(items, Constant.pageSize)  # 分页
    items = paginator.page(page)
    data = {  # 返回参数
        "pageBean": items,  # 图书列表
        "types": types,  # 所有图书类型
        "typeid": typeid,  # 图书类型主键
        "page": page,  # 当前第几页
        "itemname": itemname,  # 图书名称
    }
    return render(request, "index/index.html", context=data)


# 热点推荐（根据图书总评分降序推荐）
def recommendHot(request):
    data = {}  # 返回参数
    # 根据总评分，降序推荐
    sql = " select i.*,sum(s.score) " \
          " from item as i " \
          " join scorerecord as s " \
          " on i.id = s.itemid " \
          " group by i.id " \
          " order by sum(s.score) " \
          " desc limit 0,12 "
    hotItems = Item.objects.raw(sql)  # 查询sql
    data["hotItems"] = hotItems
    return render(request, "index/recommendHot.html", context=data)


# 个性化推荐（基于用户的协同过滤推荐算法），如果没有推荐结果进行热点推荐
# 基于用户的协同过滤推荐算法实现原理：
# 1、根据用户评分信息构建用户-图书评分矩阵
# 2、根据用户-图书评分矩阵计算用户之间的相似度
# 3、根据用户之间的相似度得到目标用户的最近邻居KNN
# 4、预测图书评分并进行推荐
def recommendCF(request):
    print("基于用户的协同过滤推荐算法开始")
    # 返回参数
    data = {}
    # 当前登录用户id
    currentUserid = request.session.get(Constant.session_user_id)
    # 数据类型转换
    currentUserid = int(currentUserid)
    # 查询所有评分数据
    print("查询所有评分数据")
    scorerecords = Scorerecord.objects.all()
    data_dic = {}  # 创建一个空字典,保存用户-图书评分矩阵
    # 遍历所有评分数据
    for scorerecord in scorerecords:
        userid = scorerecord.userid_id  # 用户id
        itemid = scorerecord.itemid_id  # 图书id
        rating = int(scorerecord.score)  # 评分
        # 为 用户-图书评分矩阵 赋值
        if userid not in data_dic.keys():
            data_dic[userid] = {itemid: rating}
        else:
            data_dic[userid][itemid] = rating
    # 如果 用户-图书评分矩阵 为空
    if len(data_dic) == 0:
        print("没有评分数据！")
        print("基于用户的协同过滤推荐算法结束")
        print("基于用户的协同过滤推荐算法没有推荐结果，进行热点推荐")
        data["userCfItems"] = recommendHotEx()
        return render(request, "index/recommendCF.html", context=data)
    # 判断当前登录用户是否有评分数据
    if currentUserid not in data_dic.keys():
        print("目标用户没有评分！")
        print("基于用户的协同过滤推荐算法结束")
        print("基于用户的协同过滤推荐算法没有推荐结果，进行热点推荐")
        data["userCfItems"] = recommendHotEx()
        return render(request, "index/recommendCF.html", context=data)
    # 计算用户相似度（余弦算法）
    print("计算目标用户与其他用户的相似度（余弦算法）：")
    similarity_dic = dict()  # 定义目标用户与其他用户的相似度字典
    similarity_dic[currentUserid] = 0  # 赋值，设置目标用户与目标用户的相似度为0，目的是不参与计算
    for userid, items in data_dic.items():  # 遍历用户-图书评分矩阵中的所有用户
        if currentUserid != userid:  # 非目标用户参与计算
            # 余弦算法
            temp = 0  # 计算分子
            temp2 = 0  # 计算分母
            temp3 = 0  # 计算分母
            for itemid, rating in data_dic[currentUserid].items():  # 遍历目标用户的评分图书
                if itemid in items.keys():  # 计算共同评分的图书
                    temp += float(rating) * float(items[itemid])
                    temp2 += pow(float(rating), 2)
                    temp3 += pow(float(items[itemid]), 2)
            # 定义两个用户之间的相似度，distance值越大表示两者越相似
            distance = 0
            if temp2 == 0 or temp3 == 0:
                distance = 0
            else:
                distance = temp / (sqrt(temp2) * sqrt(temp3))  # 计算相似度
            # 赋值
            similarity_dic[userid] = distance
            # 打印输出用户相似度
            print("userid:" + str(currentUserid) + "    与userid：" + str(userid) + "    相似度=" + str(distance))
    print("用户相似度：")
    # 总输出用户相似度
    print(similarity_dic)
    # 将相似度排序，返回list类型
    similarity_dic = sorted(similarity_dic.items(), key=operator.itemgetter(1), reverse=True)  # 最相似的N个用户
    print("目标用户邻居：")
    # 目标用户与其他用户的相似度（按照相似度大小排序后的结果，即用户的所有邻居）
    print(similarity_dic)
    # 截取前N个最近邻居
    similarity_dic = similarity_dic[:10]  # 列表转字典
    # 过滤掉相似度为0的相似度
    similarity_dic = [(key, value) for key, value in similarity_dic if value > 0]
    print("目标用户最近邻居：%s" % similarity_dic)
    similarity_dic = dict(similarity_dic)
    # 推荐，预测评分
    # 先计算目标用户的平均评分
    sum_rating = 0
    for itemid, rating in data_dic[currentUserid].items():
        sum_rating += float(rating)
    # 目标用户对图书的平均评分
    avg_rating = sum_rating / len(data_dic[currentUserid].items())
    # 推荐
    item_rec_dic = {}  # 定义推荐结果
    # 遍历用户相似度，获取所有为目标用户推荐的图书（目标用户没有评分的，同时最近邻评分的图书）
    for userid, similarity in similarity_dic.items():
        for itemid, rating in data_dic[userid].items():
            if itemid not in data_dic[currentUserid].keys():
                if itemid not in item_rec_dic.keys():
                    item_rec_dic[itemid] = {userid: rating}
                else:
                    item_rec_dic[itemid][userid] = rating
    print("所有推荐图书：")
    print(item_rec_dic)
    # 最终推荐的图书（至少有两个最近邻同时评分的同一个图书才可以推荐）
    item_rec_final_dic = {}  # 定义最终推荐的图书
    # 遍历所有推荐的图书
    for itemid, item in item_rec_dic.items():
        if len(item) > 1:
            pre_score1 = 0
            pre_score2 = 0
            for userid, rating in item.items():
                pre_score1 += similarity_dic[userid] * (rating - avg_rating)
                pre_score2 += similarity_dic[userid]
            pre_score = avg_rating + pre_score1 / pre_score2
            # 预测评分
            item_rec_final_dic[itemid] = pre_score
    print("推荐图书和预测评分：")
    print(item_rec_final_dic)
    # 排序，根据预测评分
    item_rec_final_dic = sorted(item_rec_final_dic.items(), key=operator.itemgetter(1), reverse=True);
    print("最终推荐图书和预测评分：")
    # 截取前K个推荐图书
    item_rec_final_dic = item_rec_final_dic[:12]
    print(item_rec_final_dic)
    # 查找推荐结果
    if (item_rec_final_dic is not None) and (len(item_rec_final_dic) > 0):
        cfItemidsList = list()
        for cfItemid, pre in item_rec_final_dic:
            cfItemidsList.append(int(cfItemid))
        # 查询推荐的图书
        data["userCfItems"] = Item.objects.filter(id__in=cfItemidsList)
        print("基于用户的协同过滤推荐算法结束")
    else:
        print("基于用户的协同过滤推荐算法结束")
        print("基于用户的协同过滤推荐算法没有推荐结果，进行热点推荐")
        data["userCfItems"] = recommendHotEx()
    return render(request, "index/recommendCF.html", context=data)


# 热点推荐（根据图书总评分降序推荐）
def recommendHotEx():
    data = {}  # 返回参数
    # 根据总评分，降序推荐
    sql = " select i.*,sum(s.score) " \
          " from item as i " \
          " join scorerecord as s " \
          " on i.id = s.itemid " \
          " group by i.id " \
          " order by sum(s.score) " \
          " desc limit 0,12 "
    return Item.objects.raw(sql)  # 查询sql
