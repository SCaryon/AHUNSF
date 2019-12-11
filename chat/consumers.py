from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    chats = dict()

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        try:
            ChatConsumer.chats[self.room_group_name].add(self)
        except:
            ChatConsumer.chats[self.room_group_name] = set([self])
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        ChatConsumer.chats[self.room_group_name].remove(self)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        senderpk = int(text_data_json['senderpk'])
        receiverpk = int(text_data_json['receiverpk'])
        sender = User.objects.filter(pk=senderpk).first()
        receiver = User.objects.filter(pk=receiverpk).first()
        if len(self.chats[self.room_group_name]) == 2:
            msg = Message(sender=sender,receiver=receiver,text=message,isread=True)
        else:
            msg = Message(sender=sender,receiver=receiver,text=message,isread=False)
        msg.save()
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'receiver': receiver.username
            }
        )

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver
        }))
