from django.conf.urls import patterns, url
from Counter.views import CounterListView, CounterDetailView, CounterCreateView, CounterUpdateView, CounterDeleteView

urlpatterns = patterns('',
    url(r'^$', CounterListView.as_view(), name='counter_list'),
    url(r'^detail/(?P<pk>\d+)$', CounterDetailView.as_view(), name='counter_detail'),
    url(r'^create/$', CounterCreateView.as_view(), name='counter_create'),
    url(r'^update/(?P<pk>\d+)$', CounterUpdateView.as_view(), name='counter_update'),
    url(r'^delete/(?P<pk>\d+)$', CounterDeleteView.as_view(), name='counter_delete'),
)