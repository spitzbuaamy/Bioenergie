from django.conf.urls import patterns, url
from MeasurementPrice.views import MeasurementPriceListView, MeasurementPriceDetailView, MeasurementPriceCreateView, MeasurementPriceUpdateView, MeasurementPriceDeleteView

urlpatterns = patterns('',
                       url(r'^$', MeasurementPriceListView.as_view(), name='measurement_price_list'),
                       url(r'^detail/(?P<pk>\d+)$', MeasurementPriceDetailView.as_view(),
                           name='measurement_price_detail'),
                       url(r'^create/$', MeasurementPriceCreateView.as_view(), name='measurement_price_create'),
                       url(r'^update/(?P<pk>\d+)$', MeasurementPriceUpdateView.as_view(),
                           name='measurement_price_update'),
                       url(r'^delete/(?P<pk>\d+)$', MeasurementPriceDeleteView.as_view(),
                           name='measurement_price_delete'),

)