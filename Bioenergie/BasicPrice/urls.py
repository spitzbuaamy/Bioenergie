from django.conf.urls import patterns, url
from BasicPrice.views import BasicPriceListView, BasicPriceDetailView, BasicPriceCreateView, BasicPriceUpdateView, BasicPriceDeleteView, GroupView

urlpatterns = patterns('',
    url(r'^$', BasicPriceListView.as_view(), name='basic_price_list'),
    url(r'^detail/(?P<pk>\d+)$', BasicPriceDetailView.as_view(), name='basic_price_detail'),
    url(r'^create/$', BasicPriceCreateView.as_view(), name='basic_price_create'),
    url(r'^update/(?P<pk>\d+)$', BasicPriceUpdateView.as_view(), name='basic_price_update'),
    url(r'^delete/(?P<pk>\d+)$', BasicPriceDeleteView.as_view(), name='basic_price_delete'),
    url(r'^groupview/$', GroupView.as_view(), name="GroupView"),

)
