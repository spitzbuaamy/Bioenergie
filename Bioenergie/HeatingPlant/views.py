from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import HeatingPlant
from HeatingPlant.forms import HeatingPlantForm


class HeatingPlantListView(ListView):
    template_name = "HeatingPlant/heating_plant_list.html"
    model = HeatingPlant
    context_object_name = 'heating_plants'


class HeatingPlantDetailView(DetailView):
    template_name = "HeatingPlant/heating_plant_detail.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'


class HeatingPlantCreateView(CreateView):
    template_name = "HeatingPlant/heating_plant_form.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'
    form_class = HeatingPlantForm
    #success_url = reverse_lazy('heating_plant_list')

    def get_form(self, form_class):
        form = super(HeatingPlantCreateView, self).get_form(form_class)
        form.fields['bank'].widget.attrs.update({"class": "selectpicker"})
        return form


class HeatingPlantUpdateView(UpdateView):
    template_name = "HeatingPlant/heating_plant_form.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'
    form_class = HeatingPlantForm
    # success_url = reverse_lazy('heating_plant_list')

    def get_form(self, form_class):
        form = super(HeatingPlantUpdateView, self).get_form(form_class)
        form.fields['bank'].widget.attrs.update({"class": "selectpicker"})
        return form


class HeatingPlantDeleteView(DeleteView):
    template_name = "HeatingPlant/heating_plant_confirm_delete.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'
    success_url = reverse_lazy('heating_plant_list')
