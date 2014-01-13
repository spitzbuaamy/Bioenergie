import csv
from Abrechnung.models import Measurement, Building

#CSV-Datei importieren
reading = csv.reader(open("C:\Users\Fabian\Desktop\HTL Neufelden\Diplomarbeit\Bioenergie\Datei.csv"), delimiter=";")

for line in reading:
    building = line[0]
    measured_date = line[3]
    value = line[4]
    print(measured_date, value)

    b = Building.objects.get(name=building.customer)
    b.Measuerment.measured_date.save()
    b.Measurement.value.save()

