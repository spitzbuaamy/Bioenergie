from django.conf.urls import patterns, url
from CablePrice.views import CablePriceListView, CablePriceDetailView, CablePriceCreateView, CablePriceUpdateView, CablePriceDeleteView

urlpatterns = patterns('',
                       url(r'^$', CablePriceListView.as_view(), name='cable_price_list'),
                       url(r'^detail/(?P<pk>\d+)$', CablePriceDetailView.as_view(), name='cable_price_detail'),
                       url(r'^create/$', CablePriceCreateView.as_view(), name='cable_price_create'),
                       url(r'^update/(?P<pk>\d+)$', CablePriceUpdateView.as_view(), name='cable_price_update'),
                       url(r'^delete/(?P<pk>\d+)$', CablePriceDeleteView.as_view(), name='cable_price_delete'),

)