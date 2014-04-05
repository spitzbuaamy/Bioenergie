from django.conf.urls import patterns, url
from Building.views import BuildingListView, BuildingDetailView, BuildingCreateView, BuildingUpdateView, BuildingDeleteView, BuildingListViewInvoice, searchinvoice, EnterDate, EmptyInvoice

urlpatterns = patterns('',
                       url(r'^$', BuildingListView.as_view(), name='building_list'),
                       url(r'^detail/(?P<pk>\d+)$', BuildingDetailView.as_view(), name='building_detail'),
                       url(r'^create/$', BuildingCreateView.as_view(), name='building_create'),
                       url(r'^update/(?P<pk>\d+)$', BuildingUpdateView.as_view(), name='building_update'),
                       url(r'^delete/(?P<pk>\d+)$', BuildingDeleteView.as_view(), name='building_delete'),
                       url(r'^invoice/$', BuildingListViewInvoice.as_view(), name='building_invoice'),
                       url(r'^invoice/search/$', searchinvoice),
                       url(r'^enterdate/(?P<pk>\d+)$', EnterDate.as_view(), name='enter_date'),
                       url(r'^emptyinvoice/$' , EmptyInvoice, name="empty_invoice")

)