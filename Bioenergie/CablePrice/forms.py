from django.forms import ModelForm
from Abrechnung.models import CablePrice


class CablePriceForm(ModelForm):
    class Meta:
        model = CablePrice