from django.forms import ModelForm
from Buildings.models import Building

class BuildingForm(ModelForm):

    class Meta:
        model = Building