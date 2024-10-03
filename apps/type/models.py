# 定义图书类型实体类
from django.db import models


class Type(models.Model):
    typename = models.CharField(max_length=255, blank=False, null=False,verbose_name="图书类型名称")

    # 这个是在后台编辑图书类型的时候列表显示类型名称而不是整个对象
    def __str__(self):
        return self.typename

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准
    class Meta:
        # 默认值为True,这个选项为True时Django可以对数据库表进行migrate或migrations、删除等操作
        # 如果为False的时候，不会对数据库表进行创建、删除等操作。可以用于现有表、数据库视图等，其他操作是一样的
        managed = False
        db_table = 'type'  # 对应的数据库表
        verbose_name_plural = "图书类型"  # 这个选项是指定，模型的复数形式是什么
        verbose_name = "图书类型"  # 给模型类起一个更可读的名字

