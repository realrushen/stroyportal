from django.views.generic import View
from django.db import transaction

from .models import BonusCard
from .utils import make_pagination, HttpResponseAjax, HttpResponseAjaxError, serialize_to_json
from .forms import BonusCardForm


class BonusCardAjaxListView(View):
    http_method_names = ['get', 'post']
    

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
            kwargs['data'] = data
            response = HttpResponseAjax(status=200, **kwargs)
        else:
            response = HttpResponseAjaxError(
                status=400,
                error_code='ajax_required',
                message='This url accepts only AJAX requests'
            )
        return response

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = BonusCardForm(request.POST)
            if form.is_valid():
                instance = form.save().as_dict()
                response = HttpResponseAjax(
                    status=201,
                    data=instance
                    )
            else:
                response = HttpResponseAjaxError(
                    status=400,
                    error_code='validation_error', 
                    message=form.errors
                    )
        else:
            response = HttpResponseAjaxError(
                status=400,
                error_code='ajax_required',
                message='This url accepts only AJAX requests'
            )
        return response
    
class BonusCardDeleteAjaxView(View):
    http_method_names = ['delete']
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            card = BonusCard.objects.get(pk=pk)
        except BonusCard.DoesNotExist:
            response = HttpResponseAjaxError(
                status=404, 
                error_code='not_found',
                message="Resourse doesn't exists in database"
            ) 
        else:
            card.delete()
            response = HttpResponseAjax(status=204)
        return response        