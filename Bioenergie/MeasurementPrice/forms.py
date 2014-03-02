from django.forms import ModelForm
from Abrechnung.models import MeasurementPrice


class MeasurementPriceForm(ModelForm):
    class Meta:
        model = MeasurementPrice