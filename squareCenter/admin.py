from django.contrib import admin
from .models import Product, ProductType, Wish, WishType


# Register your models here.
@admin.register(ProductType)
class ProductType_Admin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(WishType)
class ProductType_Admin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'type', 'pubTime', 'is_deleted', 'last_updated_time')
    ordering = ('-pubTime', )  # admin中类对象的显示顺序


@admin.register(Wish)
class Wish_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'publisher', 'type', 'pubTime', 'is_deleted', 'last_updated_time')
    ordering = ('-pubTime', )  # admin中类对象的显示顺序

