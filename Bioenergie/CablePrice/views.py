from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import CablePrice
from CablePrice.forms import CablePriceForm
from django.core.urlresolvers import reverse_lazy


class CablePriceListView(ListView):
    template_name = "CablePrice/cable_price_list.html"
    model = CablePrice
    context_object_name = 'cable_prices'


class CablePriceDetailView(DetailView):
    template_name = "CablePrice/cable_price_detail.html"
    model = CablePrice
    context_object_name = 'cable_price'


class CablePriceCreateView(CreateView):
    template_name = "CablePrice/cable_price_form.html"
    model = CablePrice
    context_object_name = 'cable_price'
    form_class = CablePriceForm
    #success_url = reverse_lazy('cable_price_list')


class CablePriceUpdateView(UpdateView):
    template_name = "CablePrice/cable_price_form.html"
    model = CablePrice
    context_object_name = 'cable_price'
    form_class = CablePriceForm
    # success_url = reverse_lazy('cable_price_list')


class CablePriceDeleteView(DeleteView):
    template_name = "CablePrice/cable_price_confirm_delete.html"
    model = CablePrice
    context_object_name = 'cable_price'
    success_url = reverse_lazy('cable_price_list')