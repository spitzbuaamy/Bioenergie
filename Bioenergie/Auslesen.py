import csv
from datetime import date
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from Abrechnung.models import HeatingPlant, Measurement

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'dev.db'), }},
    # Internationalization # https://docs.djangoproject.com/en/1.6/topics/i18n/
    LANGUAGE_CODE='en-us', TIME_ZONE='UTC', USE_I18N=True, USE_L10N=True, USE_TZ=True)

#TODO: Testen, ob das Funktioniert
heatingplant = get_object_or_404(HeatingPlant, pk=1)
measurement = get_object_or_404(Measurement, pk=1)
lastreading = heatingplant.last_reading

#CSV-Dateien importieren
reading = csv.reader(open("C:\Users\Fabian\Desktop\HTL Neufelden\Diplomarbeit\Bioenergie\Datei.csv"), delimiter=";")

if lastreading < date.today().year:

    for line in reading:
        building = line[1]
        measured_date = line[3]
        value = line[4]

        #print(building, measured_date, value)
        dataset = measurement(building=building.connection_number, measured_date=measured_date, value=value)
        saving = HeatingPlant(id=1, name=heatingplant.name, street=heatingplant.street, house_number=heatingplant.house_number,
                              zip=heatingplant.zip, place=heatingplant.place, phone_number=heatingplant.phone_number,
                              mail=heatingplant.mail, bank=heatingplant.bank, account_number=heatingplant.account_number,
                              code_number=heatingplant.code_number, BIC=heatingplant.BIC, IBAN=heatingplant.IBAN,
                              manager=heatingplant.manager, Ust_ID=heatingplant.Ust_ID,
                              company_register_number=heatingplant.company_register_number,
                              standard_discount=heatingplant.standard_discount,
                              correction_factor=heatingplant.correction_factor, last_reading=lastreading)
        saving.save()
        dataset.save()