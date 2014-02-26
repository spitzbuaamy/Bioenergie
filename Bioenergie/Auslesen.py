import csv
import os
from django.conf import settings
from Abrechnung.models import Measurement

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'dev.db'), }},
    # Internationalization # https://docs.djangoproject.com/en/1.6/topics/i18n/
    LANGUAGE_CODE='en-us', TIME_ZONE='UTC', USE_I18N=True, USE_L10N=True, USE_TZ=True)

#CSV-Datei importieren
reading = csv.reader(open("C:\Users\Fabian\Desktop\HTL Neufelden\Diplomarbeit\Bioenergie\Datei.csv"), delimiter=";")

for line in reading:
    building = line[0]
    measured_date = line[3]
    value = line[4]

    dataset = Measurement(building=building, measured_date=measured_date, value=value)
    dataset.save()

