# 定义用户实体类
from django.core import validators
from django.db import models
from apps import user


class User(models.Model):
    # 设置null=True，则仅表示在数据库中该字段可以为空，
    # 但使用后台管理添加数据时仍然要需要输入值，因为Django自动做了数据验证不允许字段为空
    # 想要在Django中也可以将字段保存为空值，则需要添加另一个参数：blank=True
    username = models.CharField(max_length=255, blank=False, null=False,verbose_name="用户名")
    password = models.CharField(max_length=255, blank=False, null=False,verbose_name="密码")
    email = models.CharField(max_length=255, blank=False, null=False,
                             validators=[validators.EmailValidator(message="邮箱格式不正确！")],verbose_name="邮箱")
    createtime = models.CharField(max_length=255, blank=False, null=False,verbose_name="注册时间")

    # 这个是在后台编辑用户的时候列表显示用户名而不是整个对象
    def __str__(self):
        return self.username

    # 嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准
    class Meta:
        # 默认值为True,这个选项为True时Django可以对数据库表进行migrate或migrations、删除等操作
        # 如果为False的时候，不会对数据库表进行创建、删除等操作。可以用于现有表、数据库视图等，其他操作是一样的
        managed = False
        db_table = 'user'  # 对应的数据库表
        verbose_name_plural = "前台用户"  # 这个选项是指定，模型的复数形式是什么
        verbose_name = "前台用户"  # 给模型类起一个更可读的名字
