from django.conf.urls import patterns, url
from Abrechnung.views import AJAXGeneratePDF

urlpatterns = patterns('',
                       url(r'^generate/$', AJAXGeneratePDF.as_view(), name='generate'),
                       url(r'^pdfrechnung/$', 'Abrechnung.views.pdfRechnung', name="pdf_Rechnung"),
                       url(r'^pdfzwischenabrechnung/(?P<id>\d+)$', 'Abrechnung.views.pdfZwischenabrechnung',
                           name="pdf_Zwischenabrechnung"),
                       url(r'^pdfleererechnung/$', 'Abrechnung.views.pdfLeereRechnung', name="pdf_Leere_Rechnung"),
                       url(r'^pdfanschluss/(?P<id1>\d+)/(?P<id2>\d+)$', 'Abrechnung.views.pdfAnschlussrechnung',
                           name="pdf_Anschlussrechnung"),


)
