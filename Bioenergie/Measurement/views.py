from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Measurement
from Measurement.forms import MeasurementForm
from django.core.urlresolvers import reverse_lazy


class MeasurementListView(ListView):
    template_name = "Measurement/measurement_list.html"
    model = Measurement
    context_object_name = 'measurements'


class MeasurementDetailView(DetailView):
    template_name = "Measurement/measurement_detail.html"
    model = Measurement
    context_object_name = 'measurement'


class MeasurementCreateView(CreateView):
    template_name = "Measurement/measurement_form.html"
    model = Measurement
    context_object_name = 'measurement'
    form_class = MeasurementForm
    #success_url = reverse_lazy('measurement_list')


class MeasurementUpdateView(UpdateView):
    template_name = "Measurement/measurement_form.html"
    model = Measurement
    context_object_name = 'measurement'
    form_class = MeasurementForm
    # success_url = reverse_lazy('measurement_list')


class MeasurementDeleteView(DeleteView):
    template_name = "Measurement/measurement_confirm_delete.html"
    model = Measurement
    context_object_name = 'measurement'
    success_url = reverse_lazy('measurement_list')
