from django.shortcuts import render, redirect
from squareCenter.models import ProductType, WishType, Product, Wish
from django.urls import reverse


# Create your views here.

def add_product(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = ProductType.objects.filter(pk=request.POST.get('typeid')).first()
        publisher = request.user
        price = request.POST.get('price')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        product = Product(name=name, description=description,
                          type=type, publisher=publisher,
                          price=price, img1=img1,
                          img2=img2, img3=img3)
        product.save()
        context['status'] = 'SUCCESS'
        return redirect(request.GET.get('from', reverse('products')))
    else:
        context['producttype_list'] = ProductType.objects.all()
        return render(request, 'upload/addproduct.html', context)


def add_wish(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = WishType.objects.filter(pk=request.POST.get('typeid')).first()
        publisher = request.user
        price = request.POST.get('price')
        wish = Wish(name=name, description=description, type=type, publisher=publisher, price=price)
        wish.save()
        context['status'] = 'SUCCESS'
        return redirect(request.GET.get('from', reverse('wishes')))
    else:
        context['wishtype_list'] = WishType.objects.all()
        return render(request, 'upload/addwish.html', context)
