from django.contrib import admin
from .models import Follow

@admin.register(Follow)
class Follow_Admin(admin.ModelAdmin):
    list_display = ('id', 'idol', 'fans', 'followTime')
    ordering = ('-followTime',)
