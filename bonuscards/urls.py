from django.conf.urls import patterns, include, url

from .views import BonusCardAjaxView


urlpatterns = [
    url(r'', BonusCardAjaxView.as_view(), name='bonuscards'),
]