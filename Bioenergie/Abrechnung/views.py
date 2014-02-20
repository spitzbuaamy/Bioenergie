# -*- coding: utf-8 -*-

from datetime import date, datetime
from xhtml2pdf import pisa
from Abrechnung.pdfmixin import PDFTemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from Abrechnung.models import Building, HeatingPlant, Offer, Rate, Index
from django import http
from django.template.loader import get_template
from django.template import Context
import cStringIO as StringIO
import cgi
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Login Abfrage                                                                       !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/buildings/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Benutzername oder Passwort falsch!")


    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Logout Abgrage                                                                      !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              PDF erstellen fuer Jahres- und Zwischenabrechnung                                   !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# toPDF Funktion
def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result, encoding='UTF-8')

    # Speichern
    file = open('Rechnungen/' + str(context_dict['customer']) + '.pdf', 'w')
    file.write(result.getvalue())
    file.close()

    if not pdf.err:
        return http.HttpResponse(result.getvalue(),
             mimetype='application/pdf')
    return http.HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Jahresabrechnung                                                                    !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# View
def pdfRechnung(request, id):
#-----------------------------------------------------------------------------------------------------------------------
    months = 12
    building = get_object_or_404(Building, pk=id)
    heatingplant = get_object_or_404(HeatingPlant, pk=1)
    customer = building.customer
    Ust_ID = heatingplant.Ust_ID
    workingprice = building.working_price
    measurementprice = building.measurement_price
    basicprice = building.basic_price
    connection_power = building.connection_power #Anschlussleistung
    rate = get_object_or_404(Rate, pk = id) #TODO: Stimmt noch nicht: Rate auf Gebaeude beziehen
    company_register_number = heatingplant.company_register_number
    bankname = heatingplant.bank
    account_number = heatingplant.account_number
    code_number = heatingplant.code_number
    IBAN = heatingplant.IBAN
    BIC = heatingplant.BIC
    correction_factor = heatingplant.correction_factor
    debiting = building.customer.debitor


    #date_old_measurement = counterchange.date #Datum alter Zaehlerstand
    #date_new_measurement = counterchange.date_new_counter #Datum neuer Zaehlerstand
    #heat_quantity = counterchange.heat_quantity #Zu verrechnende Waermemenge
    #new_reading = counterchange.counter_final_result #Neuer Zaehlerstand

#-----------------------------------------------------------------------------------------------------------------------
    # Rechnen...
    thisyear = date.today().year


    #Zum Filtern der Messungen nach dem Abrechnungsjahr (damit keine Werte von frueheren Jahren genommen werden)
    abr_date1 = building.last_bill
    abr_date2 = str(int(thisyear))+"-07-01"

    #Zaehlerwechsel

    counter_changes = building.counterchange_set.filter(date__range=[abr_date1, abr_date2])


    measurements = building.measurement_set.filter(measured_date__range=[abr_date1, abr_date2])
    #Fehlermeldung ausgeben, falls keine Messwerte vorhanden sind
    if len(measurements) > 1:
        summe = measurements.latest('measured_date').value - measurements[0].value
    else:
        summe = 'Keine Zählerstaende vorhanden'

    measurement_end_date = measurements.latest('measured_date').measured_date
    date_old_measurement = measurements[0].measured_date
    old_reading = measurements[0].value
    new_reading = measurements.latest('measured_date').value

    for counter_change in counter_changes:
        summe = summe - counter_change.new_counter_reading
        summe = summe + counter_change.counter_final_result

    measurement_diff = summe

    # Fuer die Abrechnungsperiode bei der Rechnung
    begin_acounting = "1. Juli " + str(int(thisyear-1)) #Beginn der Abrechnung (Datum)
    end_acounting = "30. Juni " + str(thisyear) #Ende der Abrechnung (Datum)

    #Alter Zaehlerstand - neuer Zaehlerstand
    #old_reading = new_reading - heat_quantity #Alter Zaehlerstand

    #Arbeitspeis
    workingpriceamount = workingprice.amount
    workingpricemulti = workingprice.amount * measurement_diff

    #Messpreis:
    measurementpriceamount = measurementprice.amount
    measurementpricemulti = measurementprice.amount * (float(months) / 12)

    #Grundpreis
    basicpriceamount = basicprice.amount
    basicpricemulti = basicpriceamount * connection_power * (float(months) / 12)

    #Zusammenrechnen der Ergebnisse von Messpreis und Grundpreis
    restult_measurementprice_basicprice = round(measurementpricemulti, 2) + round(basicpricemulti, 2)

    #Nettosumme von Arbeitspreis + Summe aus Messpreis und Grundpreis
    net_workingprice_measurementprice_basicprice = workingpricemulti + restult_measurementprice_basicprice

    #Rabatt
    discount_fixed = building.discount_fixed
    standard_discount = heatingplant.standard_discount
    if discount_fixed is None:
        discount = standard_discount
    else:
        discount = discount_fixed
    result_discount = net_workingprice_measurementprice_basicprice * (float(discount)/100)

    #MWST nach Rabatt
    vat_after_discount = (net_workingprice_measurementprice_basicprice - round(result_discount, 2)) * 0.2

    #Summe Netto - Rabatt + MwSt
    sum = net_workingprice_measurementprice_basicprice - result_discount + vat_after_discount

    #Akontozahlung Brutto, Netto und MWSt
    advanced_payment_on_account_net = rate.monthly_rate * months #Netto
    advanced_payment_on_account_vat = advanced_payment_on_account_net * float(0.2) #MWST
    advanced_payment_on_account_gross = advanced_payment_on_account_net * float(1.2) #Brutto

    #Unterscheidung ob Guthaben oder Nachzahlung; Ergebnis wird in die String-Variable credit_additionalpayment gespeichert
    if debiting is False:
        if (advanced_payment_on_account_gross - sum) > 0:
            credit_additionalpayment = "Guthaben"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen auf ihr Konto überwiesen"
        else:
            credit_additionalpayment = "Nachzahlung"
            debit_transfer = "Bitte den Betrag innerhalb von 14 Tagen auf unser Konto überweisen"
    else:
        if (advanced_payment_on_account_gross - sum) > 0:
            credit_additionalpayment = "Guthaben"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen auf Ihr Konto überwiesen."
        else:
            credit_additionalpayment = "Nachzahlung"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen von Ihrem Konto abgebucht."

    #Guthaben Brutto, Netto und MWSt
    credit_additionalpayment_gross = advanced_payment_on_account_gross - sum #Brutto
    credit_additionalpayment_net = credit_additionalpayment_gross / float(1.2) #Netto
    credit_additionalpayment_vat = credit_additionalpayment_gross - credit_additionalpayment_net #MWST

    #Neu berechnete Rate
    #(Heizkosten vom Vorjahr / Monate) * (neuer Index / vorriger Index)
    index_last_year = str(int(thisyear-1))
    index_this_year = str(int(thisyear))

    #indices = index_set.filter(date__range=[index_last_year, index_this_year])
    indexdif = float(Index.objects.get(year= index_last_year).index) / float(Index.objects.get(year=index_this_year).index)
    new_rate_gross = float(((sum / months) * indexdif)) * float(correction_factor) #Brutto
    new_rate_net = new_rate_gross / float(1.2) #Netto
    new_rate_vat = new_rate_gross - new_rate_net #MWST

    #Wenn kein ganzes Jahr abgerechnet wird, soll in der Rechnung aufscheinen: Anteilig x Monate
    if months < 12:
        partial1 = "Anteilig"
        partial2 = "Monate"
    else:
        partial1 = ""
        partial2 = ""

    #Adresse des Heiwerkes
    heatingplant_data = heatingplant.name + " " + heatingplant.street + " "+ str(heatingplant.house_number) + " " + str(heatingplant.zip) + " " + heatingplant.place


    #Erneutes auslesen des Index, um diesen auf der Rechnung anzuzeigen.
    year_ago = str(int(thisyear-2))
    index_for_the_last_year = Index.objects.get(year = year_ago).index
    index_for_this_year = Index.objects.get(year = index_last_year).index
    index_for_the_next_year = Index.objects.get(year = index_this_year).index

#-----------------------------------------------------------------------------------------------------------------------

    return write_pdf('Rechnung.html', {
        'counterchanges': counter_changes,
        'pagesize': 'A4',
        'building': building,
        'customer': customer,
        #'bank': bank,
        'measurement_diff': measurement_diff,
        'begin_acounting': begin_acounting,
        'end_acounting': end_acounting,
        'Ust_ID': Ust_ID,
        'date_old_measurement': date_old_measurement,
        'old_reading': old_reading,
        'new_reading': new_reading,
        'workingpriceamount': workingpriceamount,
        'workingpricemulti': workingpricemulti,
        'measurementpriceamount': measurementpriceamount,
        'months': months,
        'measurementpricemulti': measurementpricemulti,
        'basicpriceamount': basicpriceamount,
        'connection_power': connection_power,
        'basicpricemulti': basicpricemulti,
        'restult_measurementprice_basicprice': restult_measurementprice_basicprice,
        'net_workingprice_measurementprice_basicprice': net_workingprice_measurementprice_basicprice,
        'discount': discount,
        'result_discount': result_discount,
        'vat_after_discount': vat_after_discount,
        'sum': sum,
        'advanced_payment_on_account_net': advanced_payment_on_account_net,
        'advanced_payment_on_account_vat': advanced_payment_on_account_vat,
        'advanced_payment_on_account_gross': advanced_payment_on_account_gross,
        'credit_additionalpayment': credit_additionalpayment,
        'credit_additionalpayment_gross': credit_additionalpayment_gross,
        'credit_additionalpayment_net': credit_additionalpayment_net,
        'credit_additionalpayment_vat': credit_additionalpayment_vat,
        'debit_transfer': debit_transfer,
        'new_rate_gross': new_rate_gross,
        'new_rate_net': new_rate_net,
        'new_rate_vat': new_rate_vat,
        'company_register_number': company_register_number,
        'bankname': bankname,
        'account_number': account_number,
        'code_number': code_number,
        'IBAN': IBAN,
        'BIC': BIC,
        'measurement_end_date': measurement_end_date,
        "partial1": partial1,
        "partial2": partial2,
        "heatingplant_data": heatingplant_data,
        "index_for_the_last_year": index_for_the_last_year,
        "index_for_this_year": index_for_this_year,
        "index_for_the_next_year": index_for_the_next_year,
    })




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Zwischenabrechnung                                                                  !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def pdfZwischenabrechnung(request, id):
#-----------------------------------------------------------------------------------------------------------------------
    building = get_object_or_404(Building, pk=id)
    heatingplant = get_object_or_404(HeatingPlant, pk=1)
    customer = building.customer
    Ust_ID = heatingplant.Ust_ID
    workingprice = building.working_price
    measurementprice = building.measurement_price
    basicprice = building.basic_price
    connection_power = building.connection_power #Anschlussleistung
    rate = get_object_or_404(Rate, pk = id) #TODO: Stimmt noch nicht: Rate auf Gebaeude beziehen
    company_register_number = heatingplant.company_register_number
    bankname = heatingplant.bank
    account_number = heatingplant.account_number
    code_number = heatingplant.code_number
    IBAN = heatingplant.IBAN
    BIC = heatingplant.BIC
    correction_factor = heatingplant.correction_factor
    debiting = building.customer.debitor


    #date_old_measurement = counterchange.date #Datum alter Zaehlerstand
    #date_new_measurement = counterchange.date_new_counter #Datum neuer Zaehlerstand
    #heat_quantity = counterchange.heat_quantity #Zu verrechnende Waermemenge
    #new_reading = counterchange.counter_final_result #Neuer Zaehlerstand

#-----------------------------------------------------------------------------------------------------------------------
    # Rechnen...
    thisyear = date.today().year
    anfangsdatum = request.GET['anfangsdatum']
    enddatum = request.GET['enddatum']

    if (anfangsdatum == "2000-01-01") and (enddatum == "3000-01-01"):
        #Anzahl vergangener Monate ausrechnen
        today = datetime.now()
        month = today.month

        if month < 7:
            months = month + 6
        else:
            months = month - 6

        #Zum Filtern der Messungen nach dem Abrechnungsjahr (damit keine Werte von frueheren Jahren genommen werden)
        abr_date1 = building.last_bill
        abr_date2 = str(int(thisyear))+"-07-01"

        # Fuer die Abrechnungsperiode bei der Rechnung
        begin_acounting = abr_date1 #Beginn der Abrechnung (Datum)
        end_acounting = date.today() #Ende der Abrechnung (Datum)
    else:
        #Anzahl vergangener Monate ausrechnen
        variabel1 = anfangsdatum.split("-")
        firstmonth = variabel1[1]
        variabel2 = enddatum.split("-")
        secondmonth = variabel2[1]

        months = (12 - (int(secondmonth) - int(firstmonth)) *(-1))
        #Zum Filtern der Messungen nach dem Abrechnungsjahr (damit keine Werte von frueheren Jahren genommen werden)
        abr_date1 = str(anfangsdatum)
        abr_date2 = str(enddatum)


        # Fuer die Abrechnungsperiode bei der Rechnung
        day1 = variabel1[2]
        month1 = variabel1[1]
        year1 = variabel1[0]
        day2 = variabel2[2]
        month2 = variabel2[1]
        year2 = variabel2[0]

        if month1 == "01":
            chosenmonth1 = "Januar"
        elif month1 == "02":
            chosenmonth1 = "Februar"
        elif month1 == "03":
            chosenmonth1 = "Maerz"
        elif month1 == "04":
            chosenmonth1 = "April"
        elif month1 == "05":
            chosenmonth1 = "Mai"
        elif month1 == "06":
            chosenmonth1 = "Juni"
        elif month1 == "07":
            chosenmonth1 = "Juli"
        elif month1 == "08":
            chosenmonth1 = "August"
        elif month1 == "09":
            chosenmonth1 = "September"
        elif month1 == "10":
            chosenmonth1 = "Oktober"
        elif month1 == "11":
            chosenmonth1 = "November"
        elif month1 == "12":
            chosenmonth1 = "Dezember"

        if month2 == "01":
            chosenmonth2 = "Januar"
        elif month2 == "02":
            chosenmonth2 = "Februar"
        elif month2 == "03":
            chosenmonth2 = "Maerz"
        elif month2 == "04":
            chosenmonth2 = "April"
        elif month2 == "05":
            chosenmonth2 = "Mai"
        elif month2 == "06":
            chosenmonth2 = "Juni"
        elif month2 == "07":
            chosenmonth2 = "Juli"
        elif month2 == "08":
            chosenmonth2 = "August"
        elif month2 == "09":
            chosenmonth2 = "September"
        elif month2 == "10":
            chosenmonth2 = "Oktober"
        elif month2 == "11":
            chosenmonth2 = "November"
        elif month2 == "12":
            chosenmonth2 = "Dezember"

        begin_acounting = str(day1 + ". " + chosenmonth1 + " " + year1)  #Beginn der Abrechnung (Datum)
        end_acounting = str(day2 + ". " + chosenmonth2 + " " + year2) #Ende der Abrechnung (Datum)

    #Zaehlerwechsel
    counter_changes = building.counterchange_set.filter(date__range=[abr_date1, abr_date2])


    measurements = building.measurement_set.filter(measured_date__range=[abr_date1, abr_date2])
    #Fehlermeldung ausgeben, falls keine Messwerte vorhanden sind
    if len(measurements) > 1:
        summe = measurements.latest('measured_date').value - measurements[0].value
    else:
        summe = 'Keine Zählerstaende vorhanden'

    measurement_end_date = measurements.latest('measured_date').measured_date
    date_old_measurement = measurements[0].measured_date
    old_reading = measurements[0].value
    new_reading = measurements.latest('measured_date').value

    for counter_change in counter_changes:
        summe = summe - counter_change.new_counter_reading
        summe = summe + counter_change.counter_final_result

    measurement_diff = summe


    #Alter Zaehlerstand - neuer Zaehlerstand
    #old_reading = new_reading - heat_quantity #Alter Zaehlerstand

    #Arbeitspeis
    workingpriceamount = workingprice.amount
    workingpricemulti = workingprice.amount * measurement_diff

    #Messpreis:
    measurementpriceamount = measurementprice.amount
    measurementpricemulti = measurementprice.amount * (float(months) / 12)

    #Grundpreis
    basicpriceamount = basicprice.amount
    basicpricemulti = basicpriceamount * connection_power * (float(months) / 12)

    #Zusammenrechnen der Ergebnisse von Messpreis und Grundpreis
    restult_measurementprice_basicprice = round(measurementpricemulti, 2) + round(basicpricemulti, 2)

    #Nettosumme von Arbeitspreis + Summe aus Messpreis und Grundpreis
    net_workingprice_measurementprice_basicprice = workingpricemulti + restult_measurementprice_basicprice

    #Rabatt
    discount_fixed = building.discount_fixed
    standard_discount = heatingplant.standard_discount
    if discount_fixed is None:
        discount = standard_discount
    else:
        discount = discount_fixed
    result_discount = net_workingprice_measurementprice_basicprice * (float(discount)/100)

    #MWST nach Rabatt
    vat_after_discount = (net_workingprice_measurementprice_basicprice - round(result_discount, 2)) * 0.2

    #Summe Netto - Rabatt + MwSt
    sum = net_workingprice_measurementprice_basicprice - result_discount + vat_after_discount

    #Akontozahlung Brutto, Netto und MWSt
    advanced_payment_on_account_net = rate.monthly_rate * months #Netto
    advanced_payment_on_account_vat = advanced_payment_on_account_net * float(0.2) #MWST
    advanced_payment_on_account_gross = advanced_payment_on_account_net * float(1.2) #Brutto

    #Unterscheidung ob Guthaben oder Nachzahlung; Ergebnis wird in die String-Variable credit_additionalpayment gespeichert
    if debiting is False:
        if (advanced_payment_on_account_gross - sum) > 0:
            credit_additionalpayment = "Guthaben"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen auf ihr Konto überwiesen"
        else:
            credit_additionalpayment = "Nachzahlung"
            debit_transfer = "Bitte den Betrag innerhalb von 14 Tagen auf unser Konto überweisen"
    else:
        if (advanced_payment_on_account_gross - sum) > 0:
            credit_additionalpayment = "Guthaben"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen auf Ihr Konto überwiesen."
        else:
            credit_additionalpayment = "Nachzahlung"
            debit_transfer = "Der Betrag wird innerhalb von 14 Tagen von Ihrem Konto abgebucht."

    #Guthaben Brutto, Netto und MWSt
    credit_additionalpayment_gross = advanced_payment_on_account_gross - sum #Brutto
    credit_additionalpayment_net = credit_additionalpayment_gross / float(1.2) #Netto
    credit_additionalpayment_vat = credit_additionalpayment_gross - credit_additionalpayment_net #MWST

    #Neu berechnete Rate
    #(Heizkosten vom Vorjahr / Monate) * (neuer Index / vorriger Index)
    index_last_year = str(int(thisyear-1))
    index_this_year = str(int(thisyear))

    #indices = index_set.filter(date__range=[index_last_year, index_this_year])
    indexdif = float(Index.objects.get(year= index_last_year).index) / float(Index.objects.get(year=index_this_year).index)
    new_rate_gross = ((sum / months) * indexdif) * float(correction_factor) #Brutto
    new_rate_net = new_rate_gross / float(1.2) #Netto
    new_rate_vat = new_rate_gross - new_rate_net #MWST

    #Wenn kein ganzes Jahr abgerechnet wird, soll in der Rechnung aufscheinen: Anteilig x Monate
    if months < 12:
        partial1 = "Anteilig"
        partial2 = "Monate"
    else:
        partial1 = ""
        partial2 = ""

    #Adresse des Heiwerkes
    heatingplant_data = heatingplant.name + " " + heatingplant.street + " "+ str(heatingplant.house_number) + " " + str(heatingplant.zip) + " " + heatingplant.place


    #Erneutes auslesen des Index, um diesen auf der Rechnung anzuzeigen.
    year_ago = str(int(thisyear-2))
    index_for_the_last_year = Index.objects.get(year = year_ago).index
    index_for_this_year = Index.objects.get(year = index_last_year).index
    index_for_the_next_year = Index.objects.get(year = index_this_year).index

#-----------------------------------------------------------------------------------------------------------------------

    return write_pdf('Rechnung.html', {
        'counterchanges': counter_changes,
        'pagesize': 'A4',
        'building': building,
        'customer': customer,
        #'bank': bank,
        'measurement_diff': measurement_diff,
        'begin_acounting': begin_acounting,
        'end_acounting': end_acounting,
        'Ust_ID': Ust_ID,
        'date_old_measurement': date_old_measurement,
        'old_reading': old_reading,
        'new_reading': new_reading,
        'workingpriceamount': workingpriceamount,
        'workingpricemulti': workingpricemulti,
        'measurementpriceamount': measurementpriceamount,
        'months': months,
        'measurementpricemulti': measurementpricemulti,
        'basicpriceamount': basicpriceamount,
        'connection_power': connection_power,
        'basicpricemulti': basicpricemulti,
        'restult_measurementprice_basicprice': restult_measurementprice_basicprice,
        'net_workingprice_measurementprice_basicprice': net_workingprice_measurementprice_basicprice,
        'discount': discount,
        'result_discount': result_discount,
        'vat_after_discount': vat_after_discount,
        'sum': sum,
        'advanced_payment_on_account_net': advanced_payment_on_account_net,
        'advanced_payment_on_account_vat': advanced_payment_on_account_vat,
        'advanced_payment_on_account_gross': advanced_payment_on_account_gross,
        'credit_additionalpayment': credit_additionalpayment,
        'credit_additionalpayment_gross': credit_additionalpayment_gross,
        'credit_additionalpayment_net': credit_additionalpayment_net,
        'credit_additionalpayment_vat': credit_additionalpayment_vat,
        'debit_transfer': debit_transfer,
        'new_rate_gross': new_rate_gross,
        'new_rate_net': new_rate_net,
        'new_rate_vat': new_rate_vat,
        'company_register_number': company_register_number,
        'bankname': bankname,
        'account_number': account_number,
        'code_number': code_number,
        'IBAN': IBAN,
        'BIC': BIC,
        'measurement_end_date': measurement_end_date,
        "partial1": partial1,
        "partial2": partial2,
        "heatingplant_data": heatingplant_data,
        "index_for_the_last_year": index_for_the_last_year,
        "index_for_this_year": index_for_this_year,
        "index_for_the_next_year": index_for_the_next_year,
    })





#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Anschlussrechnung                                                                   !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def pdfAnschlussrechnung(request, id):
    #Rueckgabe der PDF bestimmen
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Anschlussrechnung.pdf"'
    #Canvas = Leinwand: Dient als Schnittstelle zur Operation Malen
    p = canvas.Canvas(response, pagesize=A4) #Seitengroesse auf A4 festlegen
    p.translate(cm,cm) #Angegebene Werte auf cm umrechnen
#-----------------------------------------------------------------------------------------------------------------------
    #Zeichnen
#-----------------------------------------------------------------------------------------------------------------------
    #Variablendeklaration fuer die Kopfzeile
    heatingplant = get_object_or_404(HeatingPlant, pk=1)
    adress = str(heatingplant.street + " " + str(heatingplant.house_number) + "   " + str(heatingplant.zip) + " " + heatingplant.place)
    telephone = str("Tel: " + heatingplant.phone_number + "   " + " Fax: " + heatingplant.phone_number)
    e_mail = str("E-Mail: " + heatingplant.mail)

    #Kopfzeile
    p.setFillColorRGB(1, 1, 0.75)
    p.setLineWidth(2) #Dicke Linien Zeichnen
    p.rect(0, 24.0*cm, 19.5*cm, 3*cm, fill=1)

    #Grundgeruest der Rechnung
    p.line(0, 24*cm, 0, 0)
    p.line(0, 0, 19.5*cm, 0)
    p.line(19.5*cm, 0, 19.5*cm, 24*cm)
    p.setLineWidth(1) #Duenne Linien Zeichnen
    p.line(0, 23*cm, 19.5*cm, 23*cm)
    p.line(0, 22*cm, 19.5*cm, 22*cm)
    p.line(0, 21*cm, 19.5*cm, 21*cm)
    p.line(2.8*cm, 21.5*cm, 19.5*cm, 21.5*cm)
    p.line(2.8*cm, 22*cm, 2.8*cm, 21*cm)
    p.line(5.8*cm, 22*cm, 5.8*cm, 21*cm)
    p.line(9*cm, 22*cm, 9*cm, 21*cm)
    p.line(12*cm, 22*cm, 12*cm, 21*cm)
    p.line(14*cm, 22*cm, 14*cm, 21*cm)
    p.line(17*cm, 22*cm, 17*cm, 21*cm)
    p.line(19.5*cm, 20.4*cm, 16.7*cm, 20.4*cm)
    p.line(16.7*cm, 20.4*cm, 16.7*cm, 16.0*cm)
    p.line(16.7*cm, 17.6*cm, 19.5*cm, 17.6*cm)
    p.setFillColorRGB(0.75, 0.75, 0.75)
    p.rect(16.7*cm, 16.0*cm, 2.75*cm, 0.5*cm, fill=1)
    p.setLineWidth(0.3) #Ganz duenne Linien Zeichnen
    p.line(0, 14.4*cm, 19.5*cm, 14.4*cm)
    p.line(0, 10.8*cm, 19.5*cm, 10.8*cm)
    p.line(0, 7.7*cm, 19.5*cm, 7.7*cm)
    p.line(0, 5.0*cm, 5.5*cm, 5.0*cm)
    p.line(12*cm, 5.0*cm, 19.5*cm, 5.0*cm)
    p.line(0, 1.5*cm, 5.5*cm, 1.5*cm)
    p.line(12*cm, 1.5*cm, 19.5*cm, 1.5*cm)
    p.line(16.7*cm, 17.05*cm, 19.5*cm, 17.05*cm)

    #Text in die Kopfzeile einfuegen
    p.setFillColorRGB(0, 0.5, 0) #Schriftfarbe auf Gruen einstellen
    p.setFont("Times-Bold", 18) #Times-Bold = Dick geschrieben
    p.drawString(1*cm, 26.2*cm, heatingplant.name)
    p.setFont("Times-Bold", 10)
    p.drawString(1*cm, 25.5*cm, adress)
    p.drawString(1*cm, 25.0*cm, telephone)
    p.drawString(1*cm, 24.5*cm, e_mail)
    p.drawImage("C:\Users\Fabian\Desktop\HTL Neufelden\Diplomarbeit\Bioenergie\Biomasse.jpg", 15*cm, 24.25*cm, width=3.5*cm, height=2.5*cm)

    #Standardtext auf der Rechnung
    p.setFont("Times-Roman", 12) #Times New Roman mit Schriftgroesse 12pt
    p.setFillColor("Black") #Schriftfarbe Schwarz einstellen
    p.drawString(1.7*cm, 1.1*cm, "Ort und Datum")
    p.drawString(1.7*cm, 4.55*cm, "Ort und Datum")
    p.drawString(0.2*cm, 3*cm, "Ich (Wir) erkläre(n) mich (uns) mit dem Vorstehenden einverstanden und erteile(n) Ihnen den Auftrag.")
    p.drawString(13.8*cm, 1.1*cm, "Unterschrift des Kunden")
    p.setFont("Times-Italic", 12) #Kursiv geschrieben mit Schriftgroesse 12pt
    p.drawString(0.2*cm, 7*cm, "Bindefrist des Angebotes:  3 Monate")
    p.setFont("Times-Bold", 9) #Dick geschrieben mit Schriftgroesse 9pt
    p.drawString(1*cm, 8*cm, "Der Abnehmer hat die Förderungsansuchen an die zuständigen Förderstellen selbst zu stellen.")
    p.drawString(1*cm, 8.35*cm, "Das Wärmeversorgungsunternehmen kann über Art und Höhe der Förderung keine Zusagen treffen.")
    p.setFont("Times-Bold", 10) #Dick geschrieben mit Schriftgroesse 10pt
    p.drawString(0.2*cm, 10.4*cm, "Die Anschlusskosten können entsprechend den aktuellen Förderrichtlinien durch verschiedene")
    p.drawString(0.2*cm, 10.0*cm, "Förderstellen gefördert werden.")
    p.setFont("Times-Roman", 10) #Times New Roman, Schriftgroesse 10pt
    p.drawString(1*cm, 11*cm, 'für die Versorgung mit Fernwärme aus dem Fernwärmenetz."')
    p.drawString(1*cm, 11.35*cm, 'bitte dem beiliegenden "Wämelieferübereinkommen" sowie den "Allgemeinen Bedingungen')
    p.drawString(1*cm, 11.7*cm, "Wertsicherung, Abrechnungsjahr, Zahlungskonditionen, Eigentumsgrenzen etc. entnehmen Sie")
    p.setFont("Times-Bold", 12) #Dick geschrieben mit Schriftgroesse 12pt
    p.drawString(0.2*cm, 14*cm, "Fernwärmepreis:")
    p.setFont("Times-Roman", 12) #Times New Roman, Schriftgroesse 12pt
    p.drawString(0.2*cm, 13.5*cm, "Grundpreis:")
    p.drawString(0.2*cm, 13*cm, "Arbeitspreis:")
    p.drawString(0.2*cm, 12.5*cm, "Messgebühr:")
    p.setFont("Times-Bold", 10) #Dick geschrieben mit Schriftgroesse 10pt
    p.drawString(2.5*cm, 15.5*cm, "Zahlungs-")
    p.drawString(2.5*cm, 15.1*cm, "konditionen:")
    p.setFont("Times-Roman", 10) #Times New Roman, Schriftgroesse 10pt
    p.drawString(5.0*cm, 15.5*cm, "50% des Anschlusspreises bei Vertragsabschluss")
    p.drawString(5.0*cm, 15.1*cm, "Rest bei Inbetriebnahme (Heizbeginn)")
    p.setFont("Times-Roman", 12) #Times New Roman, Schriftgroesse 12pt
    p.drawString(12.3*cm, 16.1*cm, "Anschlusspreis inkl. Ust.")
    p.drawString(14.5*cm, 16.65*cm, "+ 20% Ust.")
    p.drawString(14.7*cm, 17.2*cm, "Nettopreis")
    p.drawString(17.7*cm, 20.0*cm, "EUR")
    p.setFont("Times-Bold", 12) #Dick geschrieben mit Schriftgroesse 12pt
    p.drawString(0.2*cm, 20*cm, "Fernwärmeanschluss")
    p.setFont("Times-Roman", 12) #Times New Roman, Schriftgroesse 12pt
    p.drawString(0.2*cm, 19.5*cm, "Hausanschluss (bis 15m) - Anschlusspauschale")
    p.drawString(10*cm, 19.0*cm, "Nettopreis / Einheit")
    p.drawString(0.2*cm, 18.5*cm, "Anschlusswert / kW")
    p.drawString(0.2*cm, 18.0*cm, "Leitungsmehrlängen [m]:")
    p.drawString(0.2*cm, 21.6*cm, "Objektart:")
    p.drawString(3*cm, 21.6*cm, "Wohnhaus")
    p.drawString(3*cm, 21.1*cm, "Gewerbe")
    p.drawString(9.2*cm, 21.6*cm, "Öff. Gebäude")
    p.drawString(9.2*cm, 21.1*cm, "Bauparzelle")
    p.drawString(14.2*cm, 21.6*cm, "Heizung")
    p.drawString(14.2*cm, 21.1*cm, "Warmwasser")
    p.setFont("Times-Bold", 12) #Dick geschrieben mit Schriftgroesse 12pt
    p.drawString(0.2*cm, 22.6*cm, "Kundenname:")
    p.setFont("Times-Roman", 12) #Times New Roman, Schriftgroesse 12pt
    p.drawString(0.2*cm, 22.1*cm, "Anschrift:")
    p.drawString(11.5*cm, 22.6*cm, "Eigentümer:")
    p.drawString(11.5*cm, 22.1*cm, "Telefon:")
    p.setFillColorRGB(0, 0.5, 0) #Schriftfarbe auf Gruen einstellen
    p.setFont("Times-Bold", 20) #Times-Bold = Dick geschrieben
    p.drawString(4.5*cm, 23.28*cm, "Angebot für einen Fernwärmeanschluss")
#-----------------------------------------------------------------------------------------------------------------------
    #Variablen fuer die Rechnung deklarieren
    offer = get_object_or_404(Building, pk=id)
    customer_last_name = offer.building.customer.last_name
    customer_first_name = offer.building.customer.first_name
    customer_salutation = offer.building.customer.salutation
    customer_title = offer.building.customer.title
    customer = str(customer_salutation +" " + customer_title + " " + customer_first_name + " " + customer_last_name) #Kundenanschrift
    customer_street = offer.building.customer.street #Wohnort des Kunden
    customer_zip = offer.building.customer.zip
    customer_address = str(customer_street + str(customer_zip))
    connection_power = str(str(offer.building.connection_power) + " kW") #Anschlussleistung
    wohnhaus = ""
    gewerbe = ""
    public = ""
    bauparzelle = ""
    anschlusspauschale = offer.building.connection_flat_rate.amount
    lengh = int(offer.building.cable_length)

    #Rechnen und Entscheidungen treffen
    #Abfrage, welche Art von Gebauede es ist
    if offer.object_type == "Wohnhaus":
        wohnhaus = connection_power
    elif offer.object_type == "Gewerbe":
        gewerbe = connection_power
    elif offer.object_type == "Öff. Gebäude":
        public = connection_power
    else:
        bauparzelle = connection_power

    #Abfrage, ob Heizung und Warmwasser auch beheizt werden
    if offer.heating is True:
        heizung = "Ja"
    else:
        heizung = "Nein"

    if offer.warm_water is True:
        warmwasser = "Ja"
    else:
        warmwasser = "Nein"

    #Nettopreis berechnen
    connection_value_net_price = float(int(offer.building.connection_power) * 119.9) #TODO: Erfragen, ob es immer 119.9 sind

    #Abfrage, ob mehr als 15m Kabellaenge benoetigt werden
    if (lengh - 15) <= 0:
        more_lengh = str("0 m")
        real_lengh = 0
    else:
        more_lengh = str(str(lengh-15) + " m")
        real_lengh = int(lengh-15)

    #Aufschlag berechnen
    upcharge = str(int(str(offer.building.cable_price)) * real_lengh)

    #Nettopreis, Bruttopreis und Umsatzsteuer fuer Anschlusswert berechnen
    net_price = (float(anschlusspauschale) + float(connection_value_net_price) + float(upcharge))
    tax = float(net_price * 0.2)
    gross_price = float(net_price * 1.2)

    #Nettopreis, Bruttopreis und Umsatzsteuer fuer Grundpreis berechnen
    basic_price_net_price = float(offer.building.basic_price.amount)
    basic_price_tax = float(basic_price_net_price * 0.2)
    basic_price_gross_price = float(basic_price_net_price * 1.2)
    basic_price1 = str("€ " + str(basic_price_net_price))
    basic_price2 = str("€ " + str(basic_price_tax) + "Ust. = ")
    basic_price3 = str("€ " + str(basic_price_gross_price) + "je kW Anschlussleistung und Verrechnungsjahr")

    #Nettopreis, Bruttopreis und Umsatzsteuer fuer Arbeitspreis berechnen
    working_price_net_price = float(offer.building.working_price.amount)
    working_price_tax = float(working_price_net_price * 0.2)
    working_price_gross_price = float(working_price_net_price * 1.2)
    working_price1 = str("€ " + str(working_price_net_price))
    working_price2 = str("€ " + str(working_price_tax) + "Ust. = ")
    working_price3 = str("€ " + str(working_price_gross_price) + "je MWh")

    #Nettopreis, Bruttopreis und Umsatzsteuer fuer Messpreis berechnen
    measurement_price_net_price = float(offer.building.measurement_price.amount)
    measurement_price_tax = float(measurement_price_net_price * 0.2)
    measurement_price_gross_price = float(measurement_price_net_price * 1.2)
    measurement_price1 = str("€ " + str(measurement_price_net_price))
    measurement_price2 = str("€ " + str(measurement_price_tax) + "Ust. = ")
    measurement_price3 = str("€ " + str(measurement_price_gross_price) + "je Jahr")

#-----------------------------------------------------------------------------------------------------------------------
    #Varbiablen in die Rechnung einfuegen
    p.setFont("Times-Roman", 12) #Times New Roman mit Schriftgroesse 12pt
    p.setFillColor("Black") #Schriftfarbe Schwarz einstellen
    p.drawString(12.3*cm, 4.55*cm, heatingplant.name)
    p.drawString(3*cm, 22.6*cm, customer)
    p.drawString(3*cm, 22.1*cm, customer_address)
    p.drawString(14*cm, 22.6*cm, offer.owner)
    p.drawString(14*cm, 21.1*cm, offer.phone_number)
    p.drawString(6.5*cm, 21.6*cm, wohnhaus)
    p.drawString(6.5*cm, 21.1*cm, gewerbe)
    p.drawString(12.2*cm, 21.6*cm, public)
    p.drawString(12.2*cm, 21.1*cm, bauparzelle)
    p.drawString(17.5*cm, 21.6*cm, heizung)
    p.drawString(17.5*cm, 21.1*cm, warmwasser)
    p.drawString(6*cm, 18.5*cm, connection_power)
    p.drawString(18*cm, 19.5*cm, str(anschlusspauschale))
    p.drawString(17.5*cm, 19.0*cm, str(connection_value_net_price))
    p.drawString(11.5*cm, 18.5*cm, "€119,90") #TODO: Erfragen, ob dies ein Fixwert oder Varbiabel ist
    p.drawString(7*cm, 18.0*cm, more_lengh)
    p.drawString(11.5*cm, 18.0*cm, str(offer.building.cable_price))
    p.drawString(18*cm, 18.0*cm, upcharge)
    p.drawString(17.5*cm, 17.2*cm, str(net_price))
    p.drawString(17.5*cm, 16.65*cm, str(tax))
    p.drawString(17.5*cm, 16.1*cm, str(gross_price))
    p.drawString(4*cm, 13.5*cm, basic_price1)
    p.drawString(6.5*cm, 13.5*cm, basic_price2)
    p.drawString(10*cm, 13.5*cm, basic_price3)
    p.drawString(4*cm, 13.0*cm, working_price1)
    p.drawString(6.5*cm, 13.0*cm, working_price2)
    p.drawString(10*cm, 13.0*cm, working_price3)
    p.drawString(4*cm, 12.5*cm, measurement_price1)
    p.drawString(6.5*cm, 12.5*cm, measurement_price2)
    p.drawString(10*cm, 12.5*cm, measurement_price3)
    p.setFont("Times-Bold", 12) #Dick geschrieben mit Schriftgroesse 12pt
    p.drawString(0.*cm, 17.5*cm, str(offer.comment))



    # PDF korrekt downloaden und oeffnen
    p.showPage()
    p.save()

    #Seite zurueckgeben (response zurueckgeben)
    return response




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!              Leere Rechnung                                                                      !!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def pdfLeereRechnung(request):
    #Rueckgabe der PDF bestimmen
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="LeereRechnung.pdf"'
    #Canvas = Leinwand: Dient als Schnittstelle zur Operation Malen
    p = canvas.Canvas(response, pagesize=A4) #Seitengroesse auf A4 festlegen
    p.translate(cm,cm) #Angegebene Werte auf cm umrechnen
#-----------------------------------------------------------------------------------------------------------------------
    #Zeichnen
#-----------------------------------------------------------------------------------------------------------------------
    #Variablendeklaration fuer die Kopfzeile
    heatingplant = get_object_or_404(HeatingPlant, pk=1)
    adress = str(heatingplant.street + " " + str(heatingplant.house_number) + "   " + str(heatingplant.zip) + " " + heatingplant.place)
    telephone = str("Tel: " + heatingplant.phone_number + "   " + " Fax: " + heatingplant.phone_number)
    e_mail = str("E-Mail: " + heatingplant.mail)

    #Variablendeklaration fuer die Fusszeile
    fbn = str("Firmenbuchnummer: " + str(heatingplant.company_register_number))
    bankname = str("Bankname: " + str(heatingplant.bank))
    account_number = str("Kontonummer: " + str(heatingplant.account_number))
    BLZ = str("BLZ: " + str(heatingplant.code_number))
    BIC = str("BIC: " + str(heatingplant.BIC))
    IBAN = str("IBAN: " + str(heatingplant.IBAN))

    #Kopfzeile
    p.setFillColorRGB(1, 1, 0.75)
    p.rect(0, 23.7*cm, 19.5*cm, 3.5*cm, fill=1)
    p.setFillColorRGB(0, 0.5, 0)
    p.setFont("Times-Bold", 18)
    p.drawString(1*cm, 26.2*cm, heatingplant.name)
    p.setFont("Times-Bold", 10)
    p.drawString(1*cm, 25.5*cm, adress)
    p.drawString(1*cm, 25.0*cm, telephone)
    p.drawString(1*cm, 24.5*cm, e_mail)
    p.drawImage("C:\Users\Fabian\Desktop\HTL Neufelden\Diplomarbeit\Bioenergie\Biomasse.jpg", 15*cm, 24.2*cm, width=3.5*cm, height=2.5*cm)

    #Fusszeile
    p.line(0, 0, 19.5*cm, 0)
    p.line(19.5*cm, 0, 19.5*cm, 1.5*cm)
    p.line(19.5*cm, 1.5*cm, 0, 1.5*cm)
    p.line(0, 1.5*cm, 0, 0)
    p.setFillColor("Black")
    p.setFont("Times-Roman", 8)
    p.drawString(1*cm, 1*cm, fbn)
    p.drawString(12*cm, 1*cm, bankname)
    p.drawString(12*cm, 0.7*cm, account_number)
    p.drawString(15*cm, 0.7*cm, IBAN)
    p.drawString(12*cm, 0.4*cm, BLZ)
    p.drawString(15*cm, 0.4*cm, BIC)
#-----------------------------------------------------------------------------------------------------------------------
    # PDF korrekt downloaden und oeffnen
    p.showPage()
    p.save()

    #Seite zurueckgeben (response zurueckgeben)
    return response
