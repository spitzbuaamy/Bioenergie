#import csv
#import os
#from datetime import datetime
#import time
from django.http import HttpResponse
#from django.shortcuts import get_object_or_404
#from Bioenergie.settings import PROJECT_ROOT
#
#
def Auslese(request):
#    from Abrechnung.models import HeatingPlant, Measurement, Building
#
#    heatingplant = get_object_or_404(HeatingPlant, pk=1)
#    lastreading = heatingplant.last_reading
#
#    #CSV-Dateien importieren
#    search_dir = os.path.join(PROJECT_ROOT, 'CSV-Dateien')
#    os.chdir(search_dir)
#    files = filter(os.path.isfile, os.listdir(search_dir))
#    files = [os.path.join(search_dir, f) for f in files]  # add path to each file
#    files.sort(key=lambda x: os.path.getmtime(x))
#
#    for file in files:
#        dates = time.ctime(os.path.getmtime(file))
#        if datetime.strptime(dates, "%a %b %d %H:%M:%S %Y").date() > lastreading:
#            reading = csv.reader(open(file), delimiter=";")
#            for line in reading:
#                building = line[1]
#                measured_date = line[3]
#                value = line[4].replace(",", ".")
#                mybuilding = Building.objects.get(id=building)
#
#                #Date spliten
#                day = measured_date[0:2]
#                month = measured_date[3:5]
#                year = measured_date[6:10]
#                mydate = str(year + "-" + month + "-" + day)
#
#                dataset = Measurement(building=mybuilding, measured_date=mydate, value=value)
#                saving = HeatingPlant(id=1, name=heatingplant.name, street=heatingplant.street,
#                                      house_number=heatingplant.house_number,
#                                      zip=heatingplant.zip, place=heatingplant.place,
#                                      phone_number=heatingplant.phone_number,
#                                      mail=heatingplant.mail, bank=heatingplant.bank,
#                                      account_number=heatingplant.account_number,
#                                      code_number=heatingplant.code_number, BIC=heatingplant.BIC,
#                                      IBAN=heatingplant.IBAN,
#                                      manager=heatingplant.manager, Ust_ID=heatingplant.Ust_ID,
#                                      company_register_number=heatingplant.company_register_number,
#                                      standard_discount=heatingplant.standard_discount,
#                                      correction_factor=heatingplant.correction_factor, last_reading=datetime.now(),
#                                      bill_number=heatingplant.bill_number)
#                saving.save()
#                dataset.save()
   return HttpResponse("Die Auslese war erfolgreich")
