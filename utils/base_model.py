from django.db import models


class BaseModel(models.Model):
    # 字段在实例第一次保存的时候会保存当前时间，不管你在这里是否对其赋值
    create_at = models.DateTimeField(auto_now_add=True)
    # 无论是你添加还是修改对象，时间为你添加或者修改的时间
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 该模型将不会创建任何数据表。当其用作其它模型类的基类时，它的字段会自动添加至子类
        abstract = True
