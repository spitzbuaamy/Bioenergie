from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Building
from Building.forms import BuildingForm
from django.core.urlresolvers import reverse_lazy


class BuildingListView(ListView):
    model = Building
    context_object_name = 'building'


class BuildingDetailView(DetailView):
    model = Building
    context_object_name = 'building'


class BuildingCreateView(CreateView):
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    #success_url = reverse_lazy('building_list')


class BuildingUpdateView(UpdateView):
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    # success_url = reverse_lazy('building_list')


class BuildingDeleteView(DeleteView):
    model = Building
    context_object_name = 'building'
    success_url = reverse_lazy('building_list')