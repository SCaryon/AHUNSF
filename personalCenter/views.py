import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import User


# Create your views here.

# /user/register
def register(request):
    '''
    request 使用POST传入字段
       email
       name
       password
       year,month,day  (允许为空）
       address (允许为空）
    '''
    content = {}
    email = request.POST.get('email')
    name = request.POST.get('name')
    password = request.POST.get('password')
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')
    address = request.POST.get('address')
    birthday = None
    user_obj = User.objects.filter(email=email).first()
    if(user_obj!=None):
        if (len(year) != 0 & len(month) != 0 & len(day) != 0):
            birthday = datetime.date(year, month, day)
        user = User(email=email, name=name, password=password, birthday=birthday, address=address)
        user.save()
        content['status'] = 1
        return HttpResponse(content)
    else:
        return HttpResponse("该邮箱已注册")



# /user/uid
def center(request, uid):
    content = '个人中心'
    return HttpResponse(content + str(uid))


# /user/unfollow/uid  uid被删除的idol
def unfollow(request, uid):
    content = '取消关注'
    return HttpResponse(content + str(uid))


# /user/follow/uid uid添加的idol
def follow(request, uid):
    content = '添加关注'
    return HttpResponse(content + str(uid))
