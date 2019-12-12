from django.contrib import admin
from .models import Message


# Register your models here.

@admin.register(Message)
class Message_Admin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'send_time')
    ordering = ('-send_time',)
