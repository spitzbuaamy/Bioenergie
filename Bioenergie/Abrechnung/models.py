from django.db import models


# Create your models here.
class Customer(models.Model):
    salutation = models.CharField(max_length=10) # Anrede
    title = models.CharField(max_length=32, blank = True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    house_number = models.IntegerField()
    zip = models.IntegerField() # PLZ
    place = models.CharField(max_length=32)

    def __unicode__(self):
        return self.first_name # Todo: Vorname & Nachname

    def get_absolute_url(self):
        return "/abrechnung/detail/%i" % self.id


class Price(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() # Preis
    # Todo: Typ als "Enum"


class Counter(models.Model):
    number = models.CharField(max_length=128)


class Measurement(models.Model):
    counter = models.ForeignKey(Counter)
    measured_date = models.DateField()
    value = models.IntegerField()



class Building(models.Model):
    customer = models.ForeignKey(Customer)
    price = models.ForeignKey(Price)
    counter = models.ManyToManyField(Counter)
    place = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    discount = models.IntegerField()
    discount_fixed = models.IntegerField()
    contract_date = models.DateField()

class Index (models.Model):
    year = models.IntegerField(max_length=4)
    index = models.IntegerField(max_length=4)
