from datetime import date
from xhtml2pdf import pisa
from Abrechnung.pdfmixin import PDFTemplateResponseMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic import TemplateView
from Abrechnung.models import Customer, Building, Bill, Bank, WorkingPrice, BasicPrice, MeasurementPrice, CounterChange, Measurement, Rate, Index, HeatingPlant, CounterBill
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
    building = get_object_or_404(Building, pk=id)

    customer = building.customer
    bank = building.customer.bank

    # Rechnen...
    thisyear = date.today().year
    # todo: letztes Abrechnungsdatum heranziehen:
    abr_date1 = str(int(thisyear-1))+"-06-30"
    abr_date2 = str(int(thisyear))+"-07-01"
    measurements = building.measurement_set.filter(measured_date__range=[abr_date1, abr_date2])

    if len(measurements) > 1:
        mesurement_diff = measurements.latest('measured_date').value - measurements[0].value
    else:
        mesurement_diff = 'Keine Zaehlerstaende vorhanden'

    return write_pdf('Rechnung.html', {
        'pagesize': 'A4',
        'building': building,
        'customer': customer,
        'bank': bank,
        'mesurement_diff': mesurement_diff})
