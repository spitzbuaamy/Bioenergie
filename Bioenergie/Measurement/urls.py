from django.conf.urls import patterns, url

from Measurement.views import MeasurementListView, MeasurementDetailView, MeasurementCreateView, MeasurementUpdateView, MeasurementDeleteView

urlpatterns = patterns('',
                       url(r'^$', MeasurementListView.as_view(), name='measurement_list'),
                       url(r'^detail/(?P<pk>\d+)$', MeasurementDetailView.as_view(), name='measurement_detail'),
                       url(r'^create/$', MeasurementCreateView.as_view(), name='measurement_create'),
                       url(r'^update/(?P<pk>\d+)$', MeasurementUpdateView.as_view(), name='measurement_update'),
                       url(r'^delete/(?P<pk>\d+)$', MeasurementDeleteView.as_view(), name='measurement_delete'),
)