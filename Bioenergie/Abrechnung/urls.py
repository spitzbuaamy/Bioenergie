from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^pdfrechnung/(?P<id>\d+)$', 'Abrechnung.views.pdfRechnung', name="pdf_Rechnung"),
    url(r'^pdfzwischenabrechnung/(?P<id>\d+)$', 'Abrechnung.views.pdfZwischenabrechnung', name="pdf_Zwischenabrechnung"),
    url(r'^pdfleererechnung/$', 'Abrechnung.views.LeereRechnung', name="pdf_Leere_Rechnung")

)
