from django.views.generic import View
from django.db import transaction
from django.forms import model_to_dict
from .utils import HttpResponseAjax, HttpResponseAjaxError, serialize_to_json
from .models import BonusCard
from .utils import make_pagination
from .forms import BonusCardForm
import pdb
import json


class BonusCardAjaxView(View):
    search_fields = [
        'series', 
        'number', 
        'release_date', 
        'activity_expires_date', 
        'activity_status',
        ]

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            search_params = request.GET.dict()
            cards = BonusCard.search_objects.search(search_params)
            cards, pagination = make_pagination(
                request, 
                queryset=cards, 
                page_size=50)
            data = [card.as_dict() for card in cards]
            kwargs['pagination'] = pagination
            response = HttpResponseAjax(data=data, **kwargs)
        else:
            response = HttpResponseAjaxError(code='ajax_required', message='This url accepts only AJAX requests')
        return response

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = BonusCardForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    instance = form.save().as_dict()
                response = HttpResponseAjax(data=instance)
            else:
                response = HttpResponseAjaxError(
                    code='validation_error', 
                    message=form.errors
                    )
        else:
            response = HttpResponseAjaxError(code='ajax_required', message='This url accepts only AJAX requests')
        return response