# -*- coding: utf-8 -*-
from django.views.generic import CreateView, DetailView, UpdateView
from Abrechnung.models import Offer
from Offer.forms import OfferForm


class OfferCreateView(CreateView):
    template_name = "Offer/offer_form.html"
    model = Offer
    context_object_name = 'offer'
    form_class = OfferForm

    def get_form(self, form_class):
        form = super(OfferCreateView, self).get_form(form_class)
        form.fields['building'].widget.attrs.update({'class': 'selectpicker'})
        form.fields['object_type'].widget.attrs.update({"class": "selectpicker"})
        form.fields['connection_flat_rate'].widget.attrs.update({"class": "selectpicker"})
        return form


class OfferDetailView(DetailView):
    template_name = "Offer/offer_detail.html"
    model = Offer
    context_object_name = 'offer'


class OfferUpdateView(UpdateView):
    template_name = "Offer/offer_form.html"
    model = Offer
    context_object_name = 'offer'
    form_class = OfferForm

    def get_form(self, form_class):
        form = super(OfferUpdateView, self).get_form(form_class)
        form.fields['building'].widget.attrs.update({'class': 'selectpicker'})
        form.fields['object_type'].widget.attrs.update({"class": "selectpicker"})
        form.fields['connection_flat_rate'].widget.attrs.update({"class": "selectpicker"})
        return form