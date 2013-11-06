from django.db import models
from django.forms import ModelForm
from Abrechnung.models import CounterChange


class CounterChangeForm(ModelForm):

    class Meta:
        model = CounterChange