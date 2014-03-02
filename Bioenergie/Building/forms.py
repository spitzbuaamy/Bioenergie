from django.forms import ModelForm
from Abrechnung.models import Building


class BuildingForm(ModelForm):
    class Meta:
        model = Building