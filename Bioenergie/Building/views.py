# -*- coding: utf-8 -*-
from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import Building, Customer
from Building.forms import BuildingForm


class BuildingListView(ListView):
    template_name = "Building/building_list.html"
    model = Building
    context_object_name = 'buildings'


class BuildingDetailView(DetailView):
    template_name = "Building/building_detail.html"
    model = Building
    context_object_name = 'building'


class BuildingCreateView(CreateView):
    template_name = "Building/building_form.html"
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    #success_url = reverse_lazy('building_list')

    def get_form(self, form_class):
        form = super(BuildingCreateView, self).get_form(form_class)
        form.fields['contract_date'].widget.attrs.update({"class": "datepicker"})
        form.fields['last_bill'].widget.attrs.update({"class": "datepicker"})
        form.fields['billing_begin'].widget.attrs.update({"class": "datepicker"})
        return form


class BuildingUpdateView(UpdateView):
    template_name = "Building/building_form.html"
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    # success_url = reverse_lazy('building_list')
    #todo: Gehört der datpicker zu allen 3 feldern? Im Template waren nur 2 datpicker funktionen
    def get_form(self, form_class):
        form = super(BuildingUpdateView, self).get_form(form_class)
        form.fields['contract_date'].widget.attrs.update({"class": "datepicker"})
        form.fields['last_bill'].widget.attrs.update({"class": "datepicker"})
        form.fields['billing_begin'].widget.attrs.update({"class": "datepicker"})
        return form


class BuildingDeleteView(DeleteView):
    template_name = "Building/building_confirm_delete.html"
    model = Building
    context_object_name = 'building'
    success_url = reverse_lazy('building_list')


class BuildingListViewInvoice(ListView):
    template_name = "Building/building_invoice.html"
    model = Building
    context_object_name = 'buildings'


class EnterDate(DetailView):
    template_name = "Building/EnterDate.html"
    model = Building
    context_object_name = 'building'


def search_form(request):
    return render(request, 'building/search_form.html')


def searchinvoice(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        splitedsearch = q.split()
        building = []
        customers = []

        for searchterm in splitedsearch:
            customers = list(set(chain(customers, Customer.objects.filter(
                last_name__icontains=searchterm) | Customer.objects.filter(first_name__icontains=searchterm))))
        for customer in customers:
            building += Building.objects.filter(customer=customer)

        building += Building.objects.filter(street__icontains=q)
        return render(request, 'building/search_results.html',
                      {'Buildings': building, 'query': q})
    else:
        return HttpResponse('Bitte einen Namen eingeben!')


