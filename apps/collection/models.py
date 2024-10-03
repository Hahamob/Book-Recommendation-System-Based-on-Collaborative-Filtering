# 定义收藏实体类
from django.db import models


class Collection(models.Model):
    # 用户外键，userid是一个用户对象
    # on_delete=None, # 删除关联表中的数据时,当前表与其关联的field的行为
    # on_delete=models.CASCADE, # 删除关联数据,与之关联也删除
    # on_delete=models.DO_NOTHING, # 删除关联数据,什么也不做
    # on_delete=models.PROTECT, 删除关联数据,引发错误ProtectedError
    # blank=False 不能为空数据
    # null=False 数据不能为空
    # verbose_name 列表或者编辑显示的字段描述
    userid = models.ForeignKey('user.User', models.CASCADE,
                               db_column='userid', blank=False, null=False,verbose_name="用户名")
    # 图书外键，itemid是一个图书对象
    itemid = models.ForeignKey('item.Item', models.CASCADE,
                                db_column='itemid', blank=False, null=False,verbose_name="图书名称")
    createtime = models.CharField(max_length=50, blank=False, null=False,verbose_name="收藏时间")

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准
    class Meta:
        # 默认值为True,这个选项为True时Django可以对数据库表进行migrate或migrations、删除等操作
        # 如果为False的时候，不会对数据库表进行创建、删除等操作。可以用于现有表、数据库视图等，其他操作是一样的
        managed = False
        db_table = 'collection'  # 对应的数据库表
        verbose_name_plural = "收藏记录"  # 这个选项是指定，模型的复数形式是什么
        verbose_name = "收藏记录"  # 给模型类起一个更可读的名字
