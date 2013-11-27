from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import HeatingPlant
from HeatingPlant.forms import HeatingPlantForm
from django.core.urlresolvers import reverse_lazy


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


class HeatingPlantUpdateView(UpdateView):
    template_name = "HeatingPlant/heating_plant_form.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'
    form_class = HeatingPlantForm
    # success_url = reverse_lazy('heating_plant_list')


class HeatingPlantDeleteView(DeleteView):
    template_name = "HeatingPlant/heating_plant_confirm_delete.html"
    model = HeatingPlant
    context_object_name = 'heating_plant'
    success_url = reverse_lazy('heating_plant_list')
