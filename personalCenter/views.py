import datetime
import base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User


# Create your views here.

# /user/register
def register(request):
    '''
    :param request: email name password year,month,day  (允许为空） address (允许为空）
    :return:
    '''
    context = {}
    email = request.POST.get('email')
    name = request.POST.get('name')
    password = request.POST.get('password')
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')
    address = request.POST.get('address')
    birthday = None
    user_obj = User.objects.filter(email=email).first()
    print(user_obj)
    if (user_obj == None):
        if (len(year) != 0 & len(month) != 0 & len(day) != 0):
            birthday = datetime.date(year, month, day)
        # 对密码进行加密
        password = base64.b64encode(bytes(password, 'ascii'))
        user = User(email=email, name=name, password=password, birthday=birthday, address=address)
        user.save()
        content['status'] = 1
        content['message'] = "添加用户成功"
        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})
    else:
        content['status'] = 0
        content['message'] = "添加用户失败"
        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# /user/register
def login(request):
    '''

    :param request: email password
    :return:
    '''
    context = {}
    email = request.POST.get('email')
    password = base64.b64encode(bytes(request.POST.get('password'), 'ascii'))
    user_obj = User.objects.filter(email=email).first()
    if (user_obj == None):
        context['status'] = 0
        context['message'] = "该用户未注册"
    elif (user_obj.password != password):
        context['status'] = 0
        context['message'] = "密码错误"
    else:
        context['status'] = 1
        context['message'] = "登录成功"
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# /user/uid
def center(request, uid):
    context = {'message': '个人中心'}
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# /user/unfollow/uid  uid被删除的idol
def unfollow(request, uid):
    context = {'message': '取消关注'}
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


# /user/follow/uid uid添加的idol
def follow(request, uid):
    context = {'message': '添加关注'}
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})
