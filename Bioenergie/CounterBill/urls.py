from django.conf.urls import patterns, url
from CounterBill.views import CounterBillListView, CounterBillDetailView, CounterBillCreateView, CounterBillUpdateView, CounterBillDeleteView

urlpatterns = patterns('',
                       url(r'^$', CounterBillListView.as_view(), name='counter_bill_list'),
                       url(r'^detail/(?P<pk>\d+)$', CounterBillDetailView.as_view(), name='counter_bill_detail'),
                       url(r'^create/$', CounterBillCreateView.as_view(), name='counter_bill_create'),
                       url(r'^update/(?P<pk>\d+)$', CounterBillUpdateView.as_view(), name='counter_bill_update'),
                       url(r'^delete/(?P<pk>\d+)$', CounterBillDeleteView.as_view(), name='counter_bill_delete'),

)