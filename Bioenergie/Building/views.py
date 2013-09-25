from Abrechnung.models import Building
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class BuildingListView(ListView):
    template_name = "Building/building_list.html"
    model = Building
    context_object_name = 'buildings'

class BuildingDetailView(DetailView):
    template_name = "Building/building_detail.html"
    model = Building
    context_object_name = 'building'


class BuildingCreateView(CreateView):
    template_name = "Building/customer_form.html"
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    #success_url = reverse_lazy('customer_list')


class BuildingUpdateView(UpdateView):
    template_name = "Building/customer_form.html"
    model = Building
    context_object_name = 'building'
    form_class = BuildingForm
    # success_url = reverse_lazy('customer_list')


class BuildingDeleteView(DeleteView):
    template_name = "Building/customer_confirm_delete.html"
    model = Customer
    context_object_name = 'building'
    success_url = reverse_lazy('customer_list')