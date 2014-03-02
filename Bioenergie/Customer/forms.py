from django.forms import ModelForm
from Abrechnung.models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer