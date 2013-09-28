from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Price


class PriceForm(ModelForm):

    class Meta:
        model = Price