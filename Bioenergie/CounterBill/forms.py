from django.db import models
from django.forms import ModelForm
from Abrechnung.models import CounterBill


class BuildingForm(ModelForm):

    class Meta:
        model = CounterBill