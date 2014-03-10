from itertools import chain
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import Customer, Building
from Customer.forms import CustomerForm


class CustomerListView(ListView):
    template_name = "customer/customer_list.html"
    model = Customer
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    template_name = "customer/customer_detail.html"
    model = Customer
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['buildings'] = context['customer'].building_set.all()

        return context


class CustomerCreateView(CreateView):
    template_name = "customer/customer_form.html"
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    #success_url = reverse_lazy('customer_list')

    def get_form(self, form_class):
        form = super(CustomerCreateView, self).get_form(form_class)
        form.fields['salutation'].widget.attrs.update({'class': 'selectpicker'})
        form.fields['bank'].widget.attrs.update({'class': 'selectpicker'})
        return form


class CustomerUpdateView(UpdateView):
    template_name = "customer/customer_form.html"
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    # success_url = reverse_lazy('customer_list')

    def get_form(self, form_class):
        form = super(CustomerUpdateView, self).get_form(form_class)
        form.fields['salutation'].widget.attrs.update({'class': 'selectpicker'})
        form.fields['bank'].widget.attrs.update({'class': 'selectpicker'})
        return form

class CustomerDeleteView(DeleteView):
    template_name = "customer/customer_confirm_delete.html"
    model = Customer
    context_object_name = 'customer'
    success_url = reverse_lazy('customer_list')


def search_form(request):
    return render(request, 'customer/search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        splitedsearch = q.split()
        customer = []
        for searchterm in splitedsearch:
            customer = list(set(chain(customer, Customer.objects.filter(
                last_name__icontains=searchterm) | Customer.objects.filter(
                first_name__icontains=searchterm) | Customer.objects.filter(street__icontains=searchterm))))
        return render(request, 'customer/search_results.html',
                      {'Customers': customer, 'query': q})
    else:
        return HttpResponse('Bitte einen Namen eingeben!')