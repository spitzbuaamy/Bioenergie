from django.forms import ModelForm
from Abrechnung.models import CounterBill


class CounterBillForm(ModelForm):
    class Meta:
        model = CounterBill