from django.contrib import admin
from Abrechnung.models import Customer, Price, Measurement, Building, Counter

# Todo: use autoadmin


admin.site.register(Customer)
admin.site.register(Price)
admin.site.register(Measurement)
admin.site.register(Building)
admin.site.register(Counter)