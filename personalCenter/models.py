from django.db import models


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=30, null=True)


class Follow(models.Model):
    # 两个相同的外键，通过related_name区分,Follow.idol.all()和Follow.fans.all()获取
    idol = models.ForeignKey(User, on_delete=models.CASCADE, related_name='idol')
    fans = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fans')
    followTime = models.DateTimeField(auto_now_add=True)  # 自动设置添加时间
