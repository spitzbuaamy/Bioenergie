from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Price
from Price.forms import PriceForm
from django.core.urlresolvers import reverse_lazy


class PriceListView(ListView):
    template_name = "Price/price_list.html"
    model = Price
    context_object_name = 'prices'


class PriceDetailView(DetailView):
    template_name = "Price/price_detail.html"
    model = Price
    context_object_name = 'price'


class PriceCreateView(CreateView):
    template_name = "Price/price_form.html"
    model = Price
    context_object_name = 'price'
    form_class = PriceForm
    #success_url = reverse_lazy('price_list')


class PriceUpdateView(UpdateView):
    template_name = "Price/price_form.html"
    model = Price
    context_object_name = 'price'
    form_class = PriceForm
    # success_url = reverse_lazy('price_list')


class PriceDeleteView(DeleteView):
    template_name = "Price/price_confirm_delete.html"
    model = Price
    context_object_name = 'price'
    success_url = reverse_lazy('price_list')
