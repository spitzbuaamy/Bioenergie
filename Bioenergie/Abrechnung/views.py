from datetime import date
from xhtml2pdf import pisa
from Abrechnung.pdfmixin import PDFTemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from Abrechnung.models import Building, HeatingPlant, CounterChange, Rate, Index
from django import http
from django.template.loader import get_template
from django.template import Context

import cStringIO as StringIO
import cgi

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
                return HttpResponseRedirect('/customers/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Username oder Passwort falsch!")


    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

# toPDF Funktion
def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)

    # Speichern
    file = open('Rechnungen/' + str(context_dict['customer']) + '.pdf', 'w')
    file.write(result.getvalue())
    file.close()

    if not pdf.err:
        return http.HttpResponse(result.getvalue(),
             mimetype='application/pdf')
    return http.HttpResponse('Gremlins ate your pdf! %s' % cgi.escape(html))

# View
def pdfRechnung(request, id):
#-----------------------------------------------------------------------------------------------------------------------
    months = 12
    building = get_object_or_404(Building, pk=id)
    heatingplant = get_object_or_404(HeatingPlant, pk=1)
    customer = building.customer
    bank = building.customer.bank
    Ust_ID = heatingplant.Ust_ID
    workingprice = building.working_price
    measurementprice = building.measurement_price
    basicprice = building.basic_price
    connection_power = building.connection_power #Anschlussleistung
    rate = get_object_or_404(Rate, pk=id)
    company_register_number = heatingplant.company_register_number
    bank = building.customer.bank
    bankname = bank.name
    account_number = bank.account_number
    code_number = bank.code_number
    IBAN = bank.IBAN
    BIC = bank.BIC

    #date_old_measurement = counterchange.date #Datum alter Zaehlerstand
    #date_new_measurement = counterchange.date_new_counter #Datum neuer Zaehlerstand
    #heat_quantity = counterchange.heat_quantity #Zu verrechnende Waermemenge
    #new_reading = counterchange.counter_final_result #Neuer Zaehlerstand

#-----------------------------------------------------------------------------------------------------------------------
    # Rechnen...
    thisyear = date.today().year

    # todo: letztes Abrechnungsdatum heranziehen:
    #Zum Filern der Messungen nach dem Abrechnungsjahr (damit keine Werte von frueheren Jahren genommen werden)
    abr_date1 = str(int(thisyear-1))+"-06-30"
    abr_date2 = str(int(thisyear))+"-07-01"
    measurements = building.measurement_set.filter(measured_date__range=[abr_date1, abr_date2])
    #Fehlermeldung ausgeben, falls keine Messwerte vorhanden sind
    if len(measurements) > 1:
        measurement_diff = measurements.latest('measured_date').value - measurements[0].value
    else:
        measurement_diff = 'Keine Zaehlerstaende vorhanden'
    date_old_measurement = abr_date1
    date_new_measurement = abr_date2
    old_reading = measurements[0].value
    new_reading = measurements.latest('measured_date').value

    # Fuer die Abrechnungsperiode bei der Rechnung
    begin_acounting = "01.07."+str(int(thisyear-1)) #Beginn der Abrechnung (Datum)
    end_acounting = "30.06."+str(int(thisyear)) #Ende der Abrechnung (Datum)

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
    if discount_fixed > 0:
        discount = discount_fixed
    else:
        discount = standard_discount
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
    if (advanced_payment_on_account_gross - sum) > 0:
        credit_additionalpayment = "Guthaben"
        debit_transfer = "auf Ihr Konto ueberwiesen."
    else:
        credit_additionalpayment = "Nachzahlung"
        debit_transfer = "von Ihrem Konto abgebucht."

    #Guthaben Brutto, Netto und MWSt
    credit_additionalpayment_gross = advanced_payment_on_account_gross - sum #Brutto
    credit_additionalpayment_net = credit_additionalpayment_gross / float(1.2) #Netto
    credit_additionalpayment_vat = credit_additionalpayment_gross - credit_additionalpayment_net #MWST

    #Neu berechnete Rate
    #(Heizkosten vom Vorjahr / Monate) * (neuer Index / vorriger Index)
    index_last_year = str(int(thisyear-1))
    index_this_year = str(int(thisyear))

    #indices = index_set.filter(date__range=[index_last_year, index_this_year])
    indexdif =  float(Index.objects.get(year= index_last_year).index) / float(Index.objects.get(year=index_this_year).index)
    new_rate_gross = (sum / months) * indexdif #Brutto
    new_rate_net = new_rate_gross / float(1.2) #Netto
    new_rate_vat = new_rate_gross - new_rate_net #MWST


#-----------------------------------------------------------------------------------------------------------------------

    return write_pdf('Rechnung.html', {
        'pagesize': 'A4',
        'building': building,
        'customer': customer,
        'bank': bank,
        'measurement_diff': measurement_diff,
        'begin_acounting': begin_acounting,
        'end_acounting': end_acounting,
        'Ust_ID': Ust_ID,
        'date_old_measurement': date_old_measurement,
        'date_new_measurement': date_new_measurement,
        'old_reading': old_reading,
        'new_reading': new_reading,
        #'heat_quantity': heat_quantity,
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

    })
