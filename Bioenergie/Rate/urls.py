from django.conf.urls import patterns, url
from Rate.views import RateListView, RateDetailView, RateCreateView, RateUpdateView, RateDeleteView

urlpatterns = patterns('',
                       url(r'^$', RateListView.as_view(), name='rate_list'),
                       url(r'^detail/(?P<pk>\d+)$', RateDetailView.as_view(), name='rate_detail'),
                       url(r'^create/$', RateCreateView.as_view(), name='rate_create'),
                       url(r'^update/(?P<pk>\d+)$', RateUpdateView.as_view(), name='rate_update'),
                       url(r'^delete/(?P<pk>\d+)$', RateDeleteView.as_view(), name='rate_delete'),
)