from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Counter


class CounterForm(ModelForm):

    class Meta:
        model = Counter