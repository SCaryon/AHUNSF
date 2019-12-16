from django.shortcuts import render, get_object_or_404, redirect, reverse
# from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Product, ProductType, Wish, WishType


def make_pagination(request, objects_all):
    paginator = Paginator(objects_all, settings.NUM_IN_ONE_PAGE)
    page_of_objects = paginator.get_page(request.GET.get("page", 1))
    page_id_now = page_of_objects.number
    page_range = [i for i in range(page_id_now-settings.PAGE_GAP, page_id_now+settings.PAGE_GAP+1)]
    if settings.PAGE_GAP*2+1 > page_of_objects.paginator.num_pages:  # 如果页很少 就显示这些页
        page_range = [i for i in range(1, page_of_objects.paginator.num_pages+1)]
    elif page_range[0] < 1:  # 否则若前面超界
        page_range = [i for i in range(1, 2*settings.PAGE_GAP+1+1)]
    elif page_range[-1] > page_of_objects.paginator.num_pages:  # 否则若后面超界
        page_range = [i for i in range(page_of_objects.paginator.num_pages-2*settings.PAGE_GAP, page_of_objects.paginator.num_pages+1)]
    return page_range, page_of_objects


def init_dict(request, objects_all, Class, ClassType):
    Dict = {}
    # 统计每个类别有多少products
    object_types = ClassType.objects.all()
    object_types_list = []
    for object_type in object_types:
        object_type.object_count = Class.objects.filter(type=object_type, is_deleted=False).count()  # 直接加入新的属性
        object_types_list.append(object_type)

    Dict['object_types'] = object_types_list
    Dict['page_range'], Dict['page_of_objects'] = make_pagination(request, objects_all)  # 要显示的页码
    return Dict


def products_list(request):
    keyword = request.GET.get("keyword", "")
    if keyword == "":
        products_all = Product.objects.filter(is_deleted=False).order_by('-id')
        Dict = init_dict(request, products_all, Product, ProductType)
        return render(request, "squareCenter/products_list.html", Dict)
    else:
        products_all = Product.objects.filter(is_deleted=False, name__icontains=keyword).order_by('-id')
        Dict = init_dict(request, products_all, Product, ProductType)
        Dict['keyword'] = keyword
        return render(request, "squareCenter/products_list_with_search.html", Dict)


def wishes_list(request):
    keyword = request.GET.get("keyword", "")
    if keyword == "":
        wishes_all = Wish.objects.filter(is_deleted=False).order_by('-id')
        Dict = init_dict(request, wishes_all, Wish, WishType)
        return render(request, "squareCenter/wishes_list.html", Dict)
    else:
        wishes_all = Wish.objects.filter(is_deleted=False, name__icontains=keyword).order_by('-id')
        Dict = init_dict(request, wishes_all, Wish, WishType)
        Dict['keyword'] = keyword
        return render(request, "squareCenter/wishes_list_with_search.html", Dict)


def products_list_with_type(request, type_id):
    object_type = get_object_or_404(ProductType, pk=type_id)
    products_all = Product.objects.filter(type=object_type, is_deleted=False).order_by('-id')
    Dict = init_dict(request, products_all, Product, ProductType)
    Dict['object_type'] = object_type
    return render(request, "squareCenter/products_list_with_type.html", Dict)


def wishes_list_with_type(request, type_id):
    object_type = get_object_or_404(WishType, pk=type_id)
    wishes_all = Wish.objects.filter(type=object_type, is_deleted=False).order_by('-id')
    Dict = init_dict(request, wishes_all, Wish, WishType)
    Dict['object_type'] = object_type
    return render(request, "squareCenter/wishes_list_with_type.html", Dict)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_deleted=False)
    Dict = {}
    user = User.objects.filter(username=product.publisher)
    Dict['product'] = product
    Dict['publisher_id'] = user.first().pk
    response = render(request, "squareCenter/product_detail.html", Dict)
    return response


def wish_detail(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id, is_deleted=False)
    Dict = {}
    user = User.objects.filter(username=wish.publisher)
    Dict['wish'] = wish
    Dict['publisher_id'] = user.first().pk
    response = render(request, "squareCenter/wish_detail.html", Dict)
    return response


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def delete_product(request, product_id):
    # 检查是否登录 以及产品的发布人是否是当前的登录人
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'You have not logged in yet!')
    # 取出obj
    if not Product.objects.filter(publisher=user, pk=product_id).exists():  # 不正常情况
        return ErrorResponse(401, 'You have not published this product! Can\'t delete')
    else:
        product_obj = Product.objects.get(publisher=user, pk=product_id)
        product_obj.is_deleted = True
        product_obj.save()
        redirect_url = reverse('center', kwargs={'uid': user.id})  # 返回个人中心
        return redirect(redirect_url)


def delete_wish(request, wish_id):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'You have not logged in yet!')
    # 取出obj
    if not Wish.objects.filter(publisher=user, pk=wish_id).exists():  # 不正常情况
        return ErrorResponse(401, 'You have not published this wish! Can\'t delete')
    else:
        wish_obj = Wish.objects.get(publisher=user, pk=wish_id)
        wish_obj.is_deleted = True
        wish_obj.save()
        redirect_url = reverse('center', kwargs={'uid': user.id})  # 返回个人中心
        return redirect(redirect_url)
