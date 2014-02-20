from django.conf.urls import patterns, url

from Offer.views import OfferCreateView, OfferDetailView, OfferUpdateView

urlpatterns = patterns('',
    url(r'^create/$', OfferCreateView.as_view(), name='offer_create'),
    url(r'^detail/(?P<pk>\d+)$', OfferDetailView.as_view(), name='offer_detail'),
    url(r'^update/(?P<pk>\d+)$', OfferUpdateView.as_view(), name='offer_update'),

)
