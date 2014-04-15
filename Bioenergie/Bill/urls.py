from django.conf.urls import patterns, url
from Bill.views import Auslese, AJAXLoadAuslese

urlpatterns = patterns('',
                       url(r'^load/$', AJAXLoadAuslese.as_view(), name='load'),
                       url(r'^reading/$', Auslese, name='reading'),
)
