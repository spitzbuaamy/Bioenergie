from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Index


class IndexForm(ModelForm):

    class Meta:
        model = Index