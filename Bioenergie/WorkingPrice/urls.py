from django.conf.urls import patterns, url
from WorkingPrice.views import WorkingPriceListView, WorkingPriceDetailView, WorkingPriceCreateView, WorkingPriceUpdateView, WorkingPriceDeleteView

urlpatterns = patterns('',
                       url(r'^$', WorkingPriceListView.as_view(), name='working_price_list'),
                       url(r'^detail/(?P<pk>\d+)$', WorkingPriceDetailView.as_view(), name='working_price_detail'),
                       url(r'^create/$', WorkingPriceCreateView.as_view(), name='working_price_create'),
                       url(r'^update/(?P<pk>\d+)$', WorkingPriceUpdateView.as_view(), name='working_price_update'),
                       url(r'^delete/(?P<pk>\d+)$', WorkingPriceDeleteView.as_view(), name='working_price_delete'),
)