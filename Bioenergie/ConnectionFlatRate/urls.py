from django.conf.urls import patterns, url
from ConnectionFlatRate.views import ConnectionFlatRateListView, ConnectionFlatRateDetailView, ConnectionFlatRateCreateView, ConnectionFlatRateUpdateView, ConnectionFlatRateDeleteView

urlpatterns = patterns('',
                       url(r'^$', ConnectionFlatRateListView.as_view(), name='connection_flat_rate_list'),
                       url(r'^detail/(?P<pk>\d+)$', ConnectionFlatRateDetailView.as_view(),
                           name='connection_flat_rate_detail'),
                       url(r'^create/$', ConnectionFlatRateCreateView.as_view(), name='connection_flat_rate_create'),
                       url(r'^update/(?P<pk>\d+)$', ConnectionFlatRateUpdateView.as_view(),
                           name='connection_flat_rate_update'),
                       url(r'^delete/(?P<pk>\d+)$', ConnectionFlatRateDeleteView.as_view(),
                           name='connection_flat_rate_delete'),

)