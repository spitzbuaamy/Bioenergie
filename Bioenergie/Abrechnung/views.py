from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Customer
from Abrechnung.forms import CustomerForm
from django.core.urlresolvers import reverse_lazy


class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    context_object_name = 'customer'


class CustomerCreateView(CreateView):
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(UpdateView):
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(DeleteView):
    model = Customer
    context_object_name = 'customer'
    success_url = reverse_lazy('customer_list')