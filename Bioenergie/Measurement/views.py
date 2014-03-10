from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import Measurement
from Measurement.forms import MeasurementForm


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

    def get_form(self, form_class):
        form = super(MeasurementCreateView, self).get_form(form_class)
        form.fields['measured_date'].widget.attrs.update({"class": "datepicker"})
        form.fields['building'].widget.attrs.update({"class": "selectpicker"})
        return form


class MeasurementUpdateView(UpdateView):
    template_name = "Measurement/measurement_form.html"
    model = Measurement
    context_object_name = 'measurement'
    form_class = MeasurementForm
    # success_url = reverse_lazy('measurement_list')

    def get_form(self, form_class):
        form = super(MeasurementUpdateView, self).get_form(form_class)
        form.fields['measured_date'].widget.attrs.update({"class": "datepicker"})
        form.fields['building'].widget.attrs.update({"class": "selectpicker"})
        return form


class MeasurementDeleteView(DeleteView):
    template_name = "Measurement/measurement_confirm_delete.html"
    model = Measurement
    context_object_name = 'measurement'
    success_url = reverse_lazy('measurement_list')
