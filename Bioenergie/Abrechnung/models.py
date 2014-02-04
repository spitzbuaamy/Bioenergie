from random import choice
from django.db import models
import csv

#-----------------------------------------------------------------------------------------------------------------------
# Create your models here.


class Bank(models.Model):
    name = models.CharField("Bankname", max_length=64) #Bankname
    account_number = models.IntegerField("Kontonummer") #Kontonummer
    code_number = models.IntegerField("Bankleitzahl") #Bankleitzahl
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
    salutation = models.CharField("Anrede", max_length=10, choices=SALUTATIONS, default=2, blank=True)
    title = models.CharField("Titel", max_length=32, blank=True)

    if salutation == FIRMA: #TODO: Geht noch nicht
        first_name = models.CharField("Vorname", max_length=32, blank=True)
    else:
        first_name = models.CharField("Vorname", max_length=32)

    last_name = models.CharField("Nachname", max_length=32)
    telephone_number = models.IntegerField("Telefonnummer", blank=True)
    street = models.CharField("Strasse", max_length=32)
    house_number = models.IntegerField("Hausnummer")
    zip = models.IntegerField("Postleitzahl") # PLZ
    place = models.CharField("Ort", max_length=32)
    customer_number = models.CharField("Kundennummer", max_length=32) #TODO: Format festlegen
    bank = models.ForeignKey(Bank, verbose_name= "Bank")
    #customer_account_number = models.IntegerField("Kontonummer") #Kontonummer des Kunden #TODO: Fehlermeldung, wenn auskommentiert
    #customer_code_number = models.IntegerField("Bankleitzahl") #Bankleitzahl
    #customer_BIC = models.CharField("BIC", max_length=32)
    #customer_IBAN = models.CharField("IBAN", max_length=32)


    def __unicode__(self):
        return unicode(self.first_name) + ' ' + unicode(self.last_name)

    def get_absolute_url(self):
        return "/customers/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class WorkingPrice(models.Model): #Arbeitspreis
    min = models.IntegerField("Minimum")
    max = models.IntegerField("Maximum")
    amount = models.IntegerField("Preis") #Preis
    wage_group = models.IntegerField("Gruppe")

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/workingprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class BasicPrice(models.Model): #Grundpreis
    min = models.IntegerField("Minimum")
    max = models.IntegerField("Maximum")
    amount = models.IntegerField("Preis") #Preis
    wage_group = models.IntegerField("Gruppe")

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/basicprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class MeasurementPrice(models.Model): #Messpreis
    min = models.IntegerField("Minimum")
    max = models.IntegerField("Maximum")
    amount = models.IntegerField("Preis") #Preis
    wage_group = models.IntegerField("Gruppe")

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/measurementprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class ConnectionFlatRate(models.Model):
    min = models.IntegerField("Minimum")
    max = models.IntegerField("Maximum")
    amount = models.IntegerField("Preis") #Preis
    wage_group = models.IntegerField("Gruppe")

    def __unicode__(self):
        return unicode(self.wage_group) + ': ' + unicode(self.min) + ' / ' + unicode(self.max)

    def get_absolute_url(self):
        return "/connectionflatrates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CablePrice(models.Model):
    price_per_meter = models.IntegerField("Preis pro Meter")

    def __unicode__(self):
        return unicode(self.price_per_meter)

    def get_absolute_url(self):
        return "/cableprices/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Building(models.Model):
    customer = models.ForeignKey(Customer, verbose_name="Kunde")
    working_price = models.ForeignKey(WorkingPrice, verbose_name="Arbeitspreis")
    basic_price = models.ForeignKey(BasicPrice, verbose_name="Grundpreis")
    measurement_price = models.ForeignKey(MeasurementPrice, verbose_name="Messpreis")
    connection_flat_rate = models.ForeignKey(ConnectionFlatRate, verbose_name="Anschlusspauschale") #Anschlusspauschale
    cable_price = models.ForeignKey(CablePrice, verbose_name="Zuleitungspreis") #Zuleitungspreis
    cable_length = models.IntegerField("Kabelweite") #Kabellaenge
    street = models.CharField("Strasse", max_length=32)
    house_number = models.IntegerField("Hausnummer")
    zip = models.IntegerField("Postleitzahl")
    place = models.CharField("Ort", max_length=32)
    discount_fixed = models.IntegerField("Fixer Rabatt", blank=True, null=True)
    contract_date = models.DateField("Anschlussdatum") #Anschlussdatum
    connection_number = models.IntegerField("AnschlussID") #AnschlussID
    connection_power = models.IntegerField("Anschlussleistung") #Anschlussleistung
    last_bill = models.DateField("Letzte Abrechnung") #Letzte Abrechnung
    #billing_begin = models.DateField("Abrechnungsbeginn") #TODO: Fehlermeldung, wenn auskommentiert

    def __unicode__(self):
        return unicode(self.customer) + ' ' + unicode(self.street) + ' ' + unicode(self.house_number)

    def get_absolute_url(self):
        return "/buildings/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CounterChange(models.Model):    #Zaehlerwechsel
    date = models.DateField("Datum")
    counter_final_result = models.IntegerField("Endstand")
    heat_quantity = models.IntegerField("Zu verrechnende Menge") #Zu verrechnende Waermemenge
    date_new_counter = models.DateField("Beginn des neuen Zahelers") #Beginn neuer Zaehler
    building = models.ForeignKey(Building, verbose_name="Objekt")

    def __unicode__(self):
        return unicode(self.building)

    def get_absolute_url(self):
        return "/counterchanges/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Measurement(models.Model): #Zaehlerstand
    building = models.ForeignKey(Building, verbose_name="Objekt")
    measured_date = models.DateField("Messdatum") #Messdatum
    value = models.IntegerField("Wert")

    def __unicode__(self):
        return unicode(self.measured_date)

    def get_absolute_url(self):
        return "/measurements/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Rate(models.Model):
    building = models.ForeignKey(Building, verbose_name="Objekt")
    year = models.IntegerField("Jahr")
    monthly_rate = models.IntegerField("Monatsrate")

    def __unicode__(self):
        return unicode(self.monthly_rate)

    def get_absolute_url(self):
        return "/rates/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Index(models.Model):
    year = models.IntegerField("Jahr", max_length=4)
    index = models.IntegerField("Index", max_length=4)

    def __unicode__(self):
        return unicode(self.year) + ' ' + unicode(self.index)

    def get_absolute_url(self):
        return "/indexes/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class Bill(models.Model):
    building = models.ForeignKey(Building, verbose_name="Objekt")
    bill_number = models.CharField("Rechnungsnummer", max_length=32)
    date = models.DateField("Datum")
    working_price = models.IntegerField("Arbeitspreis")
    measurement_price = models.IntegerField("Messpreis")
    basic_price = models.IntegerField("Grundpreis")
    discount = models.IntegerField("Rabatt")
    payment_net = models.IntegerField("Geleistete Akkontozahlung Netto") #geleistete Akkontozahlung Netto
    additional_payment_net = models.IntegerField("Nachzahlung Netto") #Nachzahlungen Netto
    new_payment_net = models.IntegerField("Neue Akkontozahlung Netto") #neue Akkontozahlung Netto

    def __unicode__(self):
        return unicode(self.bill_number)

    def get_absolute_url(self):
        return "/bills/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class CounterBill(models.Model):
    bill = models.ForeignKey(Bill, verbose_name="Rechnung")
    old_measurement = models.IntegerField("Alter Messstand")
    date_old_measurement = models.DateField("Datum alter Messstand")
    new_measurement = models.IntegerField("Neuer Messstand")
    date_new_measurement = models.DateField("Datum neuer Messstand")

    def __unicode__(self):
        return unicode(self.bill) + ' ' + str(self.date_new_measurement)

    def get_absolute_url(self):
        return "/counterbills/detail/%i" % self.id


#-----------------------------------------------------------------------------------------------------------------------
class HeatingPlant(models.Model):
    name = models.CharField("Name", max_length="32")
    standard_discount = models.IntegerField("Standardrabatt")
    bill_number = models.IntegerField("Rechnungsnummer")
    house_number = models.IntegerField("Hausnummer")
    street = models.CharField("Strasse", max_length="32")
    zip = models.IntegerField("Postleitzahl")
    place = models.CharField("Ort", max_length="32")
    Ust_ID = models.IntegerField("Ust ID")
    manager = models.CharField("Betriebsleiter", max_length="32")
    company_register_number = models.CharField("Firmenbuchnummer", max_length="32")

    def __unicode__(self):
        return unicode(self.name) + '(' + str(self.manager) + ')'

    def get_absolute_url(self):
        return "/heatingplants/detail/%i" % self.id