from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import CollectRecord, CollectCount

register = template.Library()


@register.filter
def get_collect_count(obj):  # 此方法可能比views中处理较慢 但影响不大
    content_type = ContentType.objects.get_for_model(obj)
    collect_count_obj, created = CollectCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return collect_count_obj.collected_num


@register.filter
def get_collect_status(obj, user):
    # print(type(user))
    # print(user)
    content_type = ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    if CollectRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.filter
def get_content_type(obj):  # 不用手写类型了
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model
