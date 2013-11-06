from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import MeasurementPrice
from MeasurementPrice.forms import MeasurementPriceForm
from django.core.urlresolvers import reverse_lazy


class MeasurementPriceListView(ListView):
    template_name = "MeasurementPrice/measurement_price_list.html"
    model = MeasurementPrice
    context_object_name = 'measurement_price'


class MeasurementPriceDetailView(DetailView):
    template_name = "MeasurementPrice/measurement_price_detail.html"
    model = MeasurementPrice
    context_object_name = 'measurement_price'


class MeasurementPriceCreateView(CreateView):
    template_name = "MeasurementPrice/measurement_price_form.html"
    model = MeasurementPrice
    context_object_name = 'measurement_price'
    form_class = MeasurementPriceForm
    #success_url = reverse_lazy('measurement_price_list')


class MeasurementPriceUpdateView(UpdateView):
    template_name = "MeasurementPrice/measurement_price_form.html"
    model = MeasurementPrice
    context_object_name = 'measurement_price'
    form_class = MeasurementPriceForm
    # success_url = reverse_lazy('measurement_price_list')


class MeasurementPriceDeleteView(DeleteView):
    template_name = "MeasurementPrice/measurement_price_confirm_delete.html"
    model = MeasurementPrice
    context_object_name = 'measurement_price'
    success_url = reverse_lazy('measurement_price_list')