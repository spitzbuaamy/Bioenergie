from django.conf.urls import patterns, url

from Index.views import IndexListView, IndexDetailView, IndexCreateView, IndexUpdateView,IndexDeleteView

urlpatterns = patterns('',
    url(r'^$', IndexListView.as_view(), name='index_list'),
    url(r'^detail/(?P<pk>\d+)$', IndexDetailView.as_view(), name='index_detail'),
    url(r'^create/$', IndexCreateView.as_view(), name='index_create'),
    url(r'^update/(?P<pk>\d+)$', IndexUpdateView.as_view(), name='index_update'),
    url(r'^delete/(?P<pk>\d+)$', IndexDeleteView.as_view(), name='index_delete'),
)