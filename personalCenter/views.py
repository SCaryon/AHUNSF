from django.shortcuts import render, redirect
from django.contrib import auth
from django.core import serializers
from django.urls import reverse
from django.http import JsonResponse
from .forms import LoginForm, RegForm, ChangePwdForm
from django.contrib.auth.models import User
from .models import Follow
from squareCenter.models import Product, Wish
from likes.models import CollectRecord


# 注册用户
def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile(user=user)
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('products')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'personalCenter/register.html', context)


# 用户登录
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('products')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'personalCenter/login.html', context)


# 退出登录
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('products')))


# 访问个人中心
def center(request, uid):
    context = {'message': '个人中心'}
    if User.objects.filter(pk=uid).exists():
        user = User.objects.filter(pk=uid).first()
        # bug : 判断是否已经登录
        if request.user.is_authenticated:
            isFans = Follow.objects.filter(fans=request.user).filter(idol=user).exists()
            context['isFans'] = isFans
        product_list = Product.objects.filter(publisher=user)
        wish_list = Wish.objects.filter(publisher=user)
        collect_record = CollectRecord.objects.filter(user=user)
        collect_product_list = set()
        collect_wish_list = set()
        for collect in collect_record:
            if collect.content_type.model == 'product':
                collect_product_list.add(collect.content_object)
            if collect.content_type.model == 'wish':
                collect_wish_list.add(collect.content_object)
        context['other'] = user
        context['product_list'] = product_list
        context['wish_list'] = wish_list
        context['collect_product_list'] = collect_product_list
        context['collect_wish_list'] = collect_wish_list
        return render(request, "personalCenter/center.html", context)
    else:
        raise RuntimeError('用户不存在')


# 关注
def follow(request):
    userid = request.GET.get('userid')
    otherid = request.GET.get('otherid')
    me = User.objects.filter(pk=userid).first()
    other = User.objects.filter(pk=otherid).first()
    follow = Follow(idol=other, fans=me)
    follow.save()
    context = {'status': 'SUCCESS', 'message': '关注成功'}
    return JsonResponse(context)


# 取消关注
def unfollow(request):
    userid = request.GET.get('userid')
    otherid = request.GET.get('otherid')
    me = User.objects.filter(pk=userid).first()
    other = User.objects.filter(pk=otherid).first()
    follow = Follow.objects.filter(idol=other).filter(fans=me).first()
    follow.delete()
    context = {'status': 'SUCCESS', 'message': '取消关注'}
    return JsonResponse(context)


# 显示关注的人
def show_idols(request):
    context = {}
    userid = request.GET.get('userid')  # 当前个人中心的id
    meid = request.GET.get('meid')  # 登录用户的id
    user = User.objects.filter(pk=userid).first()
    follows = Follow.objects.filter(fans=user)
    idols = []
    for follow in follows:
        item = {}
        item['idol'] = follow.idol.username
        item['idolid'] = follow.idol.pk
        if meid != -1:
            me = User.objects.filter(pk=meid).first()
            if Follow.objects.filter(idol=follow.idol).filter(fans=me).exists():
                item['isFollow'] = 1
            else:
                item['isFollow'] = 0
        idols.append(item)
    context['idols'] = idols
    context['status'] = 'SUCCESS'
    return JsonResponse(context)


# 显示粉丝
def show_fans(request):
    context = {}
    userid = request.GET.get('userid')  # 当前个人中心的id
    meid = request.GET.get('meid')  # 登录用户的id
    user = User.objects.filter(pk=userid).first()
    follows = Follow.objects.filter(idol=user)
    fans = []
    for follow in follows:
        item = {}
        item['fans'] = follow.fans.username
        item['fansid'] = follow.fans.pk
        if meid != -1:
            me = User.objects.filter(pk=meid).first()
            if Follow.objects.filter(idol=follow.fans).filter(fans=me).exists():
                item['isFollow'] = 1
            else:
                item['isFollow'] = 0
        fans.append(item)
    context['fans'] = fans
    context['status'] = 'SUCCESS'
    return JsonResponse(context)


# 修改密码
def change_pwd(request):
    if request.method == "POST":
        changepwd_form = ChangePwdForm(request.POST)
        if changepwd_form.is_valid():
            user = changepwd_form.cleaned_data['user']
            user.set_password(changepwd_form.cleaned_data['newpassword'])
            user.save()
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('products')))
    else:
        changepwd_form = ChangePwdForm()
    context = {}
    context['changepwd_form'] = changepwd_form
    return render(request, 'personalCenter/changepwd.html', context)
