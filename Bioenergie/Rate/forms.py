from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Rate


class BuildingForm(ModelForm):

    class Meta:
        model = Rate