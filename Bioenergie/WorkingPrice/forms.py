from django.db import models
from django.forms import ModelForm
from Abrechnung.models import WorkingPrice


class WorkingPriceForm(ModelForm):

    class Meta:
        model = WorkingPrice