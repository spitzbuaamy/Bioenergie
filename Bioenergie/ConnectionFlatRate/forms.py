from django.forms import ModelForm
from Abrechnung.models import ConnectionFlatRate


class ConnectionFlatRateForm(ModelForm):
    class Meta:
        model = ConnectionFlatRate