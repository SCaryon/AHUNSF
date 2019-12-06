from django.shortcuts import render
from .models import CollectCount, CollectRecord
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse


def SuccessResponse(collected_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['collected_num'] = collected_num
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def collect_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'You have not logged in yet!')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        # content_type现在还是字符串 然后经过下面这句话变成ContentType的一个对象
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'Object Does Not Exist')

    if request.GET.get('is_collect') == 'true':  # 要收藏
        collect_record, is_created = CollectRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if is_created:  # 正常情况 未收藏过 进行收藏
            collect_count, is_created = CollectCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            collect_count.collected_num += 1
            collect_count.save()
            return SuccessResponse(collect_count.collected_num)
        else:  # 非正常情况  已收藏过 不能重复收藏
            return ErrorResponse(402, 'You have already collected it.')
    else:  # 要取消收藏
        if CollectRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():  # 正常情况 有收藏过 取消收藏
            collect_record_obj = CollectRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            collect_record_obj.delete()
            # 收藏总数-1
            collect_count, is_created = CollectCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not is_created:  # 正常情况
                collect_count.collected_num -= 1
                collect_count.save()
                return SuccessResponse(collect_count.collected_num)
            else:  # 非正常情况 竟然新创建了
                return ErrorResponse(404, 'data error')
        else:  # 非正常情况 本来就没收藏 不能取消收藏
            return ErrorResponse(403, 'You have not collected it.')