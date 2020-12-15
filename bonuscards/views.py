from django.views.generic import View
from django.db.models import Q

from django.utils.safestring import mark_safe
from .utils import HttpResponseAjax, HttpResponseAjaxError, serialize_to_json
from .models import BonusCard
from .utils import make_pagination
import json


class BonusCardAjaxView(View):
    search_fields = [
        'series', 
        'number', 
        'release_date', 
        'activity_expires_date', 
        'activity_status'
        ]

    def get(self, request, **kwargs):
        # search_params = {field: request.GET.get(field) for field in self.search_fields}
        search_params = request.GET.dict()
        # cards = BonusCard.objects.filter(*[Q(number__contains='58'), Q(activity_status=3)])
        
        cards = BonusCard.search_objects.search(search_params)
        cards, pagination = make_pagination(
            request, 
            queryset=cards, 
            page_size=50)
        data = serialize_to_json(cards)
        kwargs['pagination'] = pagination
        response = HttpResponseAjax(content=data, **kwargs)
        return response

    def post(self, request, **kwargs):
        print(request.POST, request.body)
        data = str(request.body)
        print(data)
        return HttpResponseAjax(content=data)