from django.forms import ModelForm
from Abrechnung.models import Bill


class BillForm(ModelForm):
    class Meta:
        model = Bill