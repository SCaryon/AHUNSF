from django.shortcuts import render
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.http import JsonResponse

# Create your views here.

def contact_list(request):
    user = request.user
    if user == None:
        raise RuntimeError("未登录不能访问")
    context = {}
    linkman_list = set()
    sendermsg_list = Message.objects.filter(receiver=user)
    unread = dict()
    for msg in sendermsg_list:
        linkman_list.add(msg.sender)
        if msg.isread == False:
            if msg.sender.pk in unread:
                unread[msg.sender.pk] += 1
            else:
                unread[msg.sender.pk] = 1
    receivermsg_list = Message.objects.filter(sender=user)
    for msg in receivermsg_list:
        linkman_list.add(msg.receiver)
    context['linkman_list'] = linkman_list
    context['unread'] = unread
    return render(request, 'chat/contactlist.html', context)


def room(request, otherid):
    user = request.user
    if user == None:
        raise RuntimeError("请先登录")
    if user.pk < otherid:
        room_name = str(user.pk) + str(otherid)
    else:
        room_name = str(otherid) + str(user.pk)
    context = {}
    other = User.objects.filter(pk=otherid).first()
    unread_msg = Message.objects.filter(Q(sender=other) & Q(receiver=user) & Q(isread=False))
    msgs = Message.objects.filter((Q(sender=user) & Q(receiver=other)) |
                                  (Q(sender=other) & Q(receiver=user)))
    for msg in msgs:
        msg.isread = True
        msg.save()
    context['room_name'] = room_name
    context['other'] = other
    context['unread_msg'] = unread_msg
    return render(request, 'chat/room.html', context)


def show_history(request):
    senderpk = request.GET.get('senderpk')
    receiverpk = request.GET.get('receiverpk')
    sender = User.objects.filter(pk=senderpk).first()
    receiver = User.objects.filter(pk=receiverpk).first()
    history_msgs = Message.objects.filter((Q(sender=sender) & Q(receiver=receiver)) |
                                     (Q(sender=receiver) & Q(receiver=sender)))
    history = []
    for msg in history_msgs:
        h = {}
        h['sender'] = msg.sender.username
        h['text'] = msg.text
        h['time'] = msg.send_time
        history.append(h)
    context = {}
    context['history'] = history
    return JsonResponse(context)
