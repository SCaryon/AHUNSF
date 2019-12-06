from django.contrib import admin
from .models import CollectCount, CollectRecord


# Register your models here.
@admin.register(CollectCount)
class CollectCountAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'content_object', 'collected_num')
    ordering = ('object_id', )


@admin.register(CollectRecord)
class CollectRecordAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'collect_time')
    ordering = ('-collect_time', )
