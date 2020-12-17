import json 
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class HttpResponseAjax(HttpResponse):
    """
    Класс замена JsonResponse для ответа клиентской стороне приложения.
    Кроме того здесь реализовано добавление заголовка content_type.
    Принимает 1 обязательный аргумент с кодом ответа HTTP.
    API предполагает, что пользователь класса добавлять в kwargs тело ответа,
    который будет сериализован в JSON.
    """
    def __init__(self, status, **kwargs):
        super(HttpResponseAjax, self).__init__(
            status=status,
            content=json.dumps(kwargs),
            content_type='application/json'
        )


class HttpResponseAjaxError(HttpResponseAjax):
    """
    
    """
    def __init__(self, *, status, error_code, message):
        super(HttpResponseAjaxError, self).__init__(
            status=status, 
            error_code=error_code, 
            message = message
            )


def serialize_to_json(query_set, fields):
    return serializers.serialize(
        "json",
        query_set,
        fields=fields
        )

def make_pagination(request, queryset, page_size):
    """
    Стандартная пагинация. Пагинацию с использованием Link header из RFC 8288, решил не использовать.
    """
    page = request.GET.get('page', 1)
    querystring = request.GET.dict()
    paginator = Paginator(queryset, page_size)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    
    return objects, {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'next': objects.next_page_number() if objects.has_next() else None,
        'previous': objects.previous_page_number() if objects.has_previous() else None,
    }

