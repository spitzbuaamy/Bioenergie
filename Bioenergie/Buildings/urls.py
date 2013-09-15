from django.conf.urls import patterns, url
from Buildings.views import BuildingListView

urlpatterns = patterns('',
    url(r'^$', BuildingListView.as_view(), name='buildings_list'),
    #url(r'^detail/(?P<pk>\d+)$', CustomerDetailView.as_view(), name='customer_detail'),
    #url(r'^create/$', CustomerCreateView.as_view(), name='customer_create'),
    #url(r'^update/(?P<pk>\d+)$', CustomerUpdateView.as_view(), name='customer_update'),
    #url(r'^delete/(?P<pk>\d+)$', CustomerDeleteView.as_view(), name='customer_delete'),
)