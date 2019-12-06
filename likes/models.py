from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User


class CollectCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 对应其它表中该对象的主键值(id)
    content_object = GenericForeignKey('content_type', 'object_id')  # 类似一种更普适的外键 方便coder

    collected_num = models.IntegerField(default=0)


class CollectRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collect_time = models.DateTimeField(auto_now_add=True)
