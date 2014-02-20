from django.views.generic import CreateView, DetailView, UpdateView
from Abrechnung.models import Offer
from Offer.forms import OfferForm

class OfferCreateView(CreateView):
    template_name = "Offer/offer_form.html"
    model = Offer
    context_object_name = 'offer'
    form_class = OfferForm

class OfferDetailView(DetailView):
    template_name = "Offer/offer_detail.html"
    model = Offer
    context_object_name = 'offer'

class OfferUpdateView(UpdateView):
    template_name = "Offer/offer_form.html"
    model = Offer
    context_object_name = 'offer'
    form_class = OfferForm

