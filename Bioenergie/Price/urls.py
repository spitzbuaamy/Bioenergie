from django.conf.urls import patterns, url

from Price.views import PriceListView, PriceDetailView, PriceCreateView, PriceUpdateView,PriceDeleteView

urlpatterns = patterns('',
    url(r'^$', PriceListView.as_view(), name='price_list'),
    url(r'^detail/(?P<pk>\d+)$', PriceDetailView.as_view(), name='price_detail'),
    url(r'^create/$', PriceCreateView.as_view(), name='price_create'),
    url(r'^update/(?P<pk>\d+)$', PriceUpdateView.as_view(), name='price_update'),
    url(r'^delete/(?P<pk>\d+)$', PriceDeleteView.as_view(), name='price_delete'),
)