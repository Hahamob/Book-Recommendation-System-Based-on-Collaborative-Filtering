# 定义评分实体类
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Scorerecord(models.Model):
    # 评分范围1-5
    score = models.IntegerField(blank=False, null=False,verbose_name="评分",
                                validators=[MaxValueValidator(5), MinValueValidator(1)])
    # 用户外键，userid其实是一个用户对象
    userid = models.ForeignKey('user.User', models.CASCADE,
                               db_column='userid', blank=False, null=False,verbose_name="用户")
    # 图书外键，itemid其实是一个图书对象
    itemid = models.ForeignKey('item.Item', models.CASCADE,
                                db_column='itemid', blank=False, null=False,verbose_name="图书")
    createtime = models.CharField(max_length=50, blank=False, null=False,verbose_name="评分时间")

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准
    class Meta:
        # 默认值为True,这个选项为True时Django可以对数据库表进行migrate或migrations、删除等操作
        # 如果为False的时候，不会对数据库表进行创建、删除等操作。可以用于现有表、数据库视图等，其他操作是一样的
        managed = False
        db_table = 'scorerecord'  # 对应的数据库表
        verbose_name_plural = "评分记录"  # 这个选项是指定，模型的复数形式是什么
        verbose_name = "评分记录"  # 给模型类起一个更可读的名字
