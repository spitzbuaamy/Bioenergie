from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Offer


class OfferForm(ModelForm):

    class Meta:
        model = Offer