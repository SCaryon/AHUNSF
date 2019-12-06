from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
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
