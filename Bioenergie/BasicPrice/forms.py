from django.forms import ModelForm
from Abrechnung.models import BasicPrice


class BasicPriceForm(ModelForm):
    class Meta:
        model = BasicPrice
