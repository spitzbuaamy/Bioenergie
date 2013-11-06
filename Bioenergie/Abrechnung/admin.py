from django.contrib import admin
from Abrechnung.models import Customer, Measurement, Building, Index
# Todo: use autoadmin


admin.site.register(Customer)
admin.site.register(Measurement)
admin.site.register(Building)
admin.site.register(Index)