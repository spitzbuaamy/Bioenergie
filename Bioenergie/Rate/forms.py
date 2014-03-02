from django.forms import ModelForm
from Abrechnung.models import Rate


class RateForm(ModelForm):
    class Meta:
        model = Rate