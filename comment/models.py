from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 对应其它表中该对象的主键值(id)
    content_object = GenericForeignKey('content_type', 'object_id')  # 类似一种更普适的外键

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    # 用户对象 发出过的评论       级联删除  删除用户时会删除相关联的评论
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)


    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']
