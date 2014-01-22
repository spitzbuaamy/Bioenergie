from django.conf.urls import patterns, url
from Abrechnung.views import pdfRechnung

urlpatterns = patterns('',
    #url(r'^rechnung/(?P<pk>\d+)$', Rechnung.as_view(), name='rechnung'),
    url(r'^pdfrechnung/(?P<id>\d+)$', pdfRechnung, name="pdfRechnung"),

)
