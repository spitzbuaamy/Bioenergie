from django.contrib import admin
from Abrechnung.models import Bank, BasicPrice, Bill, Building, CablePrice, ConnectionFlatRate, CounterBill, CounterChange, Customer, Index, Measurement, MeasurementPrice, Rate, WorkingPrice, Offer
# Todo: use autoadmin


admin.site.register(Bank)
admin.site.register(BasicPrice)
admin.site.register(Bill)
admin.site.register(Building)
admin.site.register(CablePrice)
admin.site.register(ConnectionFlatRate)
admin.site.register(CounterBill)
admin.site.register(CounterChange)
admin.site.register(Customer)
admin.site.register(Index)
admin.site.register(Measurement)
admin.site.register(MeasurementPrice)
admin.site.register(Rate)
admin.site.register(WorkingPrice)
admin.site.register(Offer)