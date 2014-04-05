from django.conf.urls import patterns, url
from Bill.views import Auslese

urlpatterns = patterns('',
                       url(r'^reading/$', Auslese, name='reading'),
)
