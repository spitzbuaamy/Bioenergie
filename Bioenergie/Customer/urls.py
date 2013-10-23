from django.conf.urls import patterns, url
from Customer.views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView
from Customer import views

urlpatterns = patterns('',
    url(r'^$', CustomerListView.as_view(), name='customer_list'),
    url(r'^detail/(?P<pk>\d+)$', CustomerDetailView.as_view(), name='customer_detail'),
    url(r'^create/$', CustomerCreateView.as_view(), name='customer_create'),
    url(r'^update/(?P<pk>\d+)$', CustomerUpdateView.as_view(), name='customer_update'),
    url(r'^delete/(?P<pk>\d+)$', CustomerDeleteView.as_view(), name='customer_delete'),
    url(r'^search/$', views.search),

)