from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Customer, Building
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

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['buildings'] =  context['customer'].building_set.all()

        return context


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


def search_form(request):
    return render(request, 'customer/search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        customer = Customer.objects.filter(last_name__icontains = q)
        return render(request, 'customer/search_results.html',
            {'Customers': customer, 'query': q})
    else:
        return HttpResponse('Bitte einen Namen eingeben!')