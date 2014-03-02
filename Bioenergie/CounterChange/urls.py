from django.conf.urls import patterns, url
from CounterChange.views import CounterChangeListView, CounterChangeDetailView, CounterChangeCreateView, CounterChangeUpdateView, CounterChangeDeleteView

urlpatterns = patterns('',
                       url(r'^$', CounterChangeListView.as_view(), name='counter_change_list'),
                       url(r'^detail/(?P<pk>\d+)$', CounterChangeDetailView.as_view(), name='counter_change_detail'),
                       url(r'^create/$', CounterChangeCreateView.as_view(), name='counter_change_create'),
                       url(r'^update/(?P<pk>\d+)$', CounterChangeUpdateView.as_view(), name='counter_change_update'),
                       url(r'^delete/(?P<pk>\d+)$', CounterChangeDeleteView.as_view(), name='counter_change_delete'),

)