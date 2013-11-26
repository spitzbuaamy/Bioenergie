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
        return str(self.name)

    def get_absolute_url(self):
        return "/banks/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Customer(models.Model): #Kunde
    salutation = models.CharField(max_length=10) #Anrede
    title = models.CharField(max_length=32, blank = True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    street = models.CharField(max_length=32)
    house_number = models.IntegerField()
    zip = models.IntegerField() # PLZ
    place = models.CharField(max_length=32)
    customer_number = models.CharField(max_length=32) #TODO: Format festlegen
    bank = models.ForeignKey(Bank)

    def __unicode__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def get_absolute_url(self):
        return "/customers/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class WorkingPrice(models.Model): #Arbeitspreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return str(self.wage_group) + ': ' + str(self.min) + ' / ' + str(self.max)

    def get_absolute_url(self):
        return "/workingprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class BasicPrice(models.Model): #Grundpreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return str(self.wage_group) + ': ' + str(self.min) + ' / ' + str(self.max)

    def get_absolute_url(self):
        return "/basicprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class MeasurementPrice(models.Model): #Messpreis
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return str(self.wage_group) + ': ' + str(self.min) + ' / ' + str(self.max)

    def get_absolute_url(self):
        return "/measurementprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class ConnectionFlatRate(models.Model):
    min = models.IntegerField()
    max = models.IntegerField()
    amount = models.IntegerField() #Preis
    wage_group = models.IntegerField()

    def __unicode__(self):
        return str(self.wage_group) + ': ' + str(self.min) + ' / ' + str(self.max)

    def get_absolute_url(self):
        return "/connectionflatrates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CablePrice(models.Model):
    price_per_meter = models.IntegerField()

    def __unicode__(self):
        return str(self.price_per_meter)

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
        return self.customer # Todo: Vorname & Nachname des Customer

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
        return str(self.building)

    def get_absolute_url(self):
        return "/counterchanges/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Measurement(models.Model): #Zaehlerstand
    building = models.ForeignKey(Building)
    measured_date = models.DateField() #Messdatum
    value = models.IntegerField()

    def __unicode__(self):
        return str(self.measured_date)

    def get_absolute_url(self):
        return "/measurements/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Rate(models.Model):
    building = models.ForeignKey(Building)
    year = models.IntegerField()
    monthly_rate = models.IntegerField()

    def __unicode__(self):
        return str(self.monthly_rate)

    def get_absolute_url(self):
        return "/rates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Index(models.Model):
    year = models.IntegerField(max_length=4)
    index = models.IntegerField(max_length=4)

    def __unicode__(self):
        return str(self.year) + ' ' + str(self.index)

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
        return str(self.bill_number)

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
        return str(self.bill) + ' ' + str(self.date_new_measurement)

    def get_absolute_url(self):
        return "/counterbills/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------