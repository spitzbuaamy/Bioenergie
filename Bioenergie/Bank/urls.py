from django.conf.urls import patterns, url
from Bank.views import BankListView, BankDetailView, BankCreateView, BankUpdateView, BankDeleteView

urlpatterns = patterns('',
                       url(r'^$', BankListView.as_view(), name='bank_list'),
                       url(r'^detail/(?P<pk>\d+)$', BankDetailView.as_view(), name='bank_detail'),
                       url(r'^create/$', BankCreateView.as_view(), name='bank_create'),
                       url(r'^update/(?P<pk>\d+)$', BankUpdateView.as_view(), name='bank_update'),
                       url(r'^delete/(?P<pk>\d+)$', BankDeleteView.as_view(), name='bank_delete'),

)