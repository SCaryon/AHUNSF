from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ProductType(models.Model):
    type_name = models.CharField(max_length=60)

    def __str__(self):
        return self.type_name


class WishType(models.Model):
    type_name = models.CharField(max_length=60)

    def __str__(self):
        return self.type_name


imgpath1 = 'Uploads/ProductImages/'

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE,
                                     default=1)  # 默认是pk为1的那个type
    pubTime = models.DateTimeField(auto_now_add=True)  # create_time = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 1是pk
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # 假删
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 十位数字 小数点后两位
    img1 = models.ImageField(upload_to=imgpath1)
    img2 = models.ImageField(upload_to=imgpath1, null=True, blank=True)
    img3 = models.ImageField(upload_to=imgpath1, null=True, blank=True)


class Wish(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    type = models.ForeignKey(WishType, on_delete=models.CASCADE,
                                     default=1)  # 默认是pk为1的那个type
    pubTime = models.DateTimeField(auto_now_add=True)  # create_time = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # 1是pk
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # 假删
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 十位数字 小数点后两位
