from Abrechnung.models import Building
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class BuildingListView(ListView):
    model = Building
    context_object_name = 'buildings'