from django.db import models
from django.forms import ModelForm
from Abrechnung.models import MeasurementPrice


class BuildingForm(ModelForm):

    class Meta:
        model = MeasurementPrice