from django.conf.urls import patterns, url
from Bill.views import BillListView, BillDetailView, BillCreateView, BillUpdateView, BillDeleteView

urlpatterns = patterns('',
    url(r'^$', BillListView.as_view(), name='bill_list'),
    url(r'^detail/(?P<pk>\d+)$', BillDetailView.as_view(), name='bill_detail'),
    url(r'^create/$', BillCreateView.as_view(), name='bill_create'),
    url(r'^update/(?P<pk>\d+)$', BillUpdateView.as_view(), name='bill_update'),
    url(r'^delete/(?P<pk>\d+)$', BillDeleteView.as_view(), name='bill_delete'),
)