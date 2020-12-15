import json 
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

class HttpResponseAjax(HttpResponse):
    def __init__(self, content, status='ok', **kwargs):
        kwargs['status'] = status
        # TODO: remove extra convertation
        kwargs['content'] = json.loads(content)
        super(HttpResponseAjax, self).__init__(
            content=json.dumps(kwargs),
            content_type='application/json'
        )


class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, massage):
        super(HttpResponseAjaxError, self).__init__(
            status='error', 
            code=code, 
            massage = massage)


def serialize_to_json(query_set):
    return serializers.serialize(
        "json",
        query_set,
        fields=(
            'series', 
            'number', 
            'release_date', 
            'activity_expires_date', 
            'activity_status'
            )
        )

def make_pagination(request, queryset, page_size):
    """
    Standart pagination
    TODO: return 'previous' and 'next' page value as url
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
        'test': querystring

    }


