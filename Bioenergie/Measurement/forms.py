from django.forms import ModelForm
from Abrechnung.models import Measurement


class MeasurementForm(ModelForm):
    class Meta:
        model = Measurement