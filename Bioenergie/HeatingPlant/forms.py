from django.forms import ModelForm
from Abrechnung.models import HeatingPlant


class HeatingPlantForm(ModelForm):
    class Meta:
        model = HeatingPlant