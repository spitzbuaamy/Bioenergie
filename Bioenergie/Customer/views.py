from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Customer
from Customer.forms import CustomerForm
from django.core.urlresolvers import reverse_lazy


class CustomerListView(ListView):
    template_name = "Customer/customer_list.html"
    model = Customer
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    template_name = "Customer/customer_detail.html"
    model = Customer
    context_object_name = 'customer'


class CustomerCreateView(CreateView):
    template_name = "Customer/customer_form.html"
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    #success_url = reverse_lazy('customer_list')


class CustomerUpdateView(UpdateView):
    template_name = "Customer/customer_form.html"
    model = Customer
    context_object_name = 'customer'
    form_class = CustomerForm
    # success_url = reverse_lazy('customer_list')


class CustomerDeleteView(DeleteView):
    template_name = "Customer/customer_confirm_delete.html"
    model = Customer
    context_object_name = 'customer'
    success_url = reverse_lazy('customer_list')