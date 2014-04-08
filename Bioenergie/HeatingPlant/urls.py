from django.conf.urls import patterns, url
from HeatingPlant.views import HeatingPlantListView, HeatingPlantDetailView, HeatingPlantCreateView, HeatingPlantUpdateView, HeatingPlantDeleteView

urlpatterns = patterns('',
                       url(r'^$', HeatingPlantListView.as_view(), name='heating_plant_list'),
                       url(r'^detail/(?P<pk>\d+)$', HeatingPlantDetailView.as_view(), name='heating_plant_detail'),
                       url(r'^create/$', HeatingPlantCreateView.as_view(), name='heating_plant_create'),
                       url(r'^update/(?P<pk>\d+)$', HeatingPlantUpdateView.as_view(), name='heating_plant_update'),
                       url(r'^delete/(?P<pk>\d+)$', HeatingPlantDeleteView.as_view(), name='heating_plant_delete'),
                       url(r'^otherbills/$', 'HeatingPlant.views.OtherBill', name='other_bills'),

)