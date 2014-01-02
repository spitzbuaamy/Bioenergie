from django.conf.urls import patterns, url
from Abrechnung.views import Rechnung, pdfRechnung

urlpatterns = patterns('',
    url(r'^rechnung/(?P<pk>\d+)$', Rechnung.as_view(), name='rechnung'),
    url(r'^pdfrechnung/(?P<id>\d+)$', pdfRechnung),
)
