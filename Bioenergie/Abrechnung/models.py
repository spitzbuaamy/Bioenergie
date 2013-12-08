from random import choice
from django.db import models

#-----------------------------------------------------------------------------------------------------------------------
# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=64) #Bankname
    account_number = models.IntegerField() #Kontonummer
    code_number = models.IntegerField() #Bankleitzahl
    IBAN = models.CharField(max_length=32)
    BIC = models.CharField(max_length=32)

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return "/banks/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Customer(models.Model): #Kunde
    BLANK = ''
    HERR = 'Herr'
    FRAU = 'Frau'
    FAMILIE = 'Familie'
    FIRMA = 'Firma'
    SALUTATIONS = (
        (BLANK, ''),
        (HERR, 'Herr'),
        (FRAU, 'Frau'),
        (FAMILIE, 'Familie'),
        (FIRMA, 'Firma'),
    )
    salutation = models.CharField(max_length=10, choices=SALUTATIONS, default=2, blank=True)
    title = models.CharField(max_length=32, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    telephone_number = models.IntegerField(blank=True)
    street = models.CharField(max_length=32)
    house_number = models.IntegerField()
    zip = models.IntegerField() # PLZ
    place = models.CharField(max_length=32)
    customer_number = models.CharField(max_length=32) #TODO: Format festlegen
    bank = models.ForeignKey(Bank)

    def __unicode__(self):
        return unicode(self.first_name) + ' ' + unicode(self.last_name)

    def get_absolute_url(self):
        return "/customers/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class WorkingPrice(models.Model): #Arbeitspreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/workingprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class BasicPrice(models.Model): #Grundpreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/basicprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class MeasurementPrice(models.Model): #Messpreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/measurementprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class ConnectionFlatRate(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/connectionflatrates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CablePrice(models.Model):
    price_per_meter = models.IntegerField()

    def __unicode__(self):
        return unicode(self.price_per_meter)

    def get_absolute_url(self):
        return "/cableprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Building(models.Model):
    customer = models.ForeignKey(Customer)
    working_price = models.ForeignKey(WorkingPrice)
    basic_price = models.ForeignKey(BasicPrice)
    measurement_price = models.ForeignKey(MeasurementPrice)
    connection_flat_rate = models.ForeignKey(ConnectionFlatRate) #Anschlusspauschale
    cable_price = models.ForeignKey(CablePrice) #Zuleitungspreis
    cable_length = models.IntegerField() #Kabellaenge
    street = models.CharField(max_length=32)
    house_number = models.IntegerField()
    zip = models.IntegerField()
    place = models.CharField(max_length=32)
    discount_fixed = models.IntegerField()
    contract_date = models.DateField() #Anschlussdatum
    connection_number = models.IntegerField() #AnschlussID
    connection_power = models.IntegerField() #Anschlussleistung
    last_bill = models.DateField() #Letzte Abrechnung

    def __unicode__(self):
        return unicode(self.customer) + ' ' + unicode(self.street) + ' ' + unicode(self.house_number) # Todo: Vorname & Nachname des Customer

    def get_absolute_url(self):
        return "/buildings/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CounterChange(models.Model):    #Zaehlerwechsel
    date = models.DateField()
    counter_final_result = models.IntegerField()
    heat_quantity = models.IntegerField() #Zu verrechnende Waermemenge
    date_new_counter = models.DateField() #Beginn neuer Zaehler
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return unicode(self.building)

    def get_absolute_url(self):
        return "/counterchanges/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Measurement(models.Model): #Zaehlerstand
    building = models.ForeignKey(Building)
    measured_date = models.DateField() #Messdatum
    value = models.IntegerField()

    def __unicode__(self):
        return unicode(self.measured_date)

    def get_absolute_url(self):
        return "/measurements/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Rate(models.Model):
    building = models.ForeignKey(Building)
    year = models.IntegerField()
    monthly_rate = models.IntegerField()

    def __unicode__(self):
        return unicode(self.monthly_rate)

    def get_absolute_url(self):
        return "/rates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Index(models.Model):
    year = models.IntegerField(max_length=4)
    index = models.IntegerField(max_length=4)

    def __unicode__(self):
        return unicode(self.year) + ' ' + unicode(self.index)

    def get_absolute_url(self):
        return "/indexes/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Bill(models.Model):
    building = models.ForeignKey(Building)
    bill_number = models.CharField(max_length=32)  #TODO: Rechnungsnummer-Zusammensetzung fragen
    date = models.DateField()
    working_price = models.IntegerField()
    measurement_price = models.IntegerField()
    basic_price = models.IntegerField()
    discount = models.IntegerField()
    payment_net = models.IntegerField() #geleistete Akkontozahlung Netto
    additional_payment_net = models.IntegerField() #Nachzahlungen Netto
    new_payment_net = models.IntegerField() #neue Akkontozahlung Netto

    def __unicode__(self):
        return unicode(self.bill_number)

    def get_absolute_url(self):
        return "/bills/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CounterBill(models.Model):
    bill = models.ForeignKey(Bill)
    old_measurement = models.IntegerField()
    date_old_measurement = models.DateField()
    new_measurement = models.IntegerField()
    date_new_measurement = models.DateField()

    def __unicode__(self):
        return unicode(self.bill) + ' ' + str(self.date_new_measurement)

    def get_absolute_url(self):
        return "/counterbills/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class HeatingPlant(models.Model):
    name = models.CharField(max_length="32")
    standard_discount = models.IntegerField()
    bill_number = models.IntegerField()
    house_number = models.IntegerField()
    street = models.CharField(max_length="32")
    zip = models.IntegerField()
    place = models.CharField(max_length="32")
    Ust_ID = models.IntegerField()
    manager = models.CharField(max_length="32")
    company_register_number = models.IntegerField()

    def __unicode__(self):
        return unicode(self.name) + '(' + str(self.manager) + ')'

    def get_absolute_url(self):
        return "/heatingplants/detail/%i" % self.id