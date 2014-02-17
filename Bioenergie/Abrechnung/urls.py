from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^pdfrechnung/(?P<id>\d+)$', 'Abrechnung.views.pdfRechnung', name="pdf_Rechnung"),
    url(r'^pdfzwischenabrechnung/(?P<id>\d+)$', 'Abrechnung.views.pdfZwischenabrechnung', name="pdf_Zwischenabrechnung"),

)
