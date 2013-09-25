from django.conf.urls import patterns, url

from Building.views import BuildingListView, BuildingDetailView, BuildingCreateView, BuildingUpdateView,BuildingDeleteView

urlpatterns = patterns('',
    url(r'^$', BuildingListView.as_view(), name='building_list'),
    url(r'^detail/(?P<pk>\d+)$', BuildingDetailView.as_view(), name='building_detail'),
    url(r'^create/$', BuildingCreateView.as_view(), name='building_create'),
    url(r'^update/(?P<pk>\d+)$', BuildingUpdateView.as_view(), name='building_update'),
    url(r'^delete/(?P<pk>\d+)$', BuildingDeleteView.as_view(), name='building_delete'),
)