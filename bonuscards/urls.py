from django.conf.urls import patterns, include, url

from .views import BonusCardAjaxListView, BonusCardDeleteAjaxView


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', BonusCardDeleteAjaxView.as_view(), name='bonuscard-delete'),
    url(r'', BonusCardAjaxListView.as_view(), name='bonuscard-list'),
)
