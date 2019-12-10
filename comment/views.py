from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.conf import settings

from .models import Comment
from .forms import CommentForm
from likes.templatetags.collects_tags import *


# Create your views here.
def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        Comment_obj = Comment()
        Comment_obj.user = request.user
        Comment_obj.text = comment_form.cleaned_data['text']
        Comment_obj.content_object = comment_form.cleaned_data['content_object']
        Comment_obj.save()

        data['status'] = 'SUCCESS'
        data['username'] = request.user.username
        data['comment_time'] = localtime(Comment_obj.comment_time).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = Comment_obj.text
        data['content_type'] = get_content_type(Comment_obj)  # ajax增加评论收藏用
        data['pk'] = Comment_obj.pk
    else:
        # return render(request, 'error.html', {'message': comment_form.errors.as_text(), 'redirect_to': referer})
        data['message'] = list(comment_form.errors.values())[0][0]
        data['status'] = 'ERROR'
    return JsonResponse(data)


def SuccessResponse():
    data = {}
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def delete_comment(request):
    # 先检测是否登录，然后检测删除的评论是否对应当前的用户
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'You have not logged in yet!')

    content_type = request.GET.get('content_type')
    object_id1 = int(request.GET.get('object_id1'))  # 评论对象的pk
    object_id2 = int(request.GET.get('object_id2'))  # 评论的pk

    try:
        # content_type现在还是字符串 然后经过下面这句话变成ContentType的一个对象
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id1)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'Object Does Not Exist')

    # 下面进行评论删除
    if Comment.objects.filter(content_type=content_type, object_id=object_id1, user=user, pk=object_id2).exists():  # 正常情况
        comment_obj = Comment.objects.get(content_type=content_type, object_id=object_id1, user=user, pk=object_id2)
        comment_obj.delete()
        return SuccessResponse()
    else:  # 非正常情况
        return ErrorResponse(403, 'You have not commented that.')