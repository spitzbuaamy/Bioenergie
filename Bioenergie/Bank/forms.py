from django.db import models
from django.forms import ModelForm
from Abrechnung.models import Bank


class BankForm(ModelForm):

    class Meta:
        model = Bank