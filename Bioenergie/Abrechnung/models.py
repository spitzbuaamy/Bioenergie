from django.db import models


# Create your models here.
class Customer(models.Model):
    salutation = models.CharField(max_length=10) # Anrede
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    zip = models.CharField(max_length=4) # PLZ
    place = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    house_number = models.CharField(max_length=32)
    title = models.CharField(max_length=32)

    def __unicode__(self):
        return self.first_name # Todo: Vorname & Nachname

    # Todo: define a get_absolute_url method on the Model


class Price(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() # Preis
    # Todo: Typ als "Enum"


class Measurement(models.Model):
    measured_date = models.DateField()
    value = models.IntegerField()


class Counter(models.Model):
    measurement = models.ForeignKey(Measurement)
    number = models.CharField(max_length=128)


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