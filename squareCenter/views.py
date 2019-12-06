from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.conf import settings

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
    product = get_object_or_404(Product, pk=product_id)

    Dict = {}
    Dict['product'] = product
    response = render(request, "squareCenter/product_detail.html", Dict)
    return response


def wish_detail(request, wish_id):
    wish = get_object_or_404(Wish, pk=wish_id)

    Dict = {}
    Dict['wish'] = wish
    response = render(request, "squareCenter/wish_detail.html", Dict)
    return response


