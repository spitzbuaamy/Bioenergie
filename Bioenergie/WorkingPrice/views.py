from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import WorkingPrice
from WorkingPrice.forms import WorkingPriceForm


class WorkingPriceListView(ListView):
    template_name = "WorkingPrice/working_price_list.html"
    model = WorkingPrice
    context_object_name = 'working_prices'


class WorkingPriceDetailView(DetailView):
    template_name = "WorkingPrice/working_price_detail.html"
    model = WorkingPrice
    context_object_name = 'working_price'


class WorkingPriceCreateView(CreateView):
    template_name = "WorkingPrice/working_price_form.html"
    model = WorkingPrice
    context_object_name = 'working_price'
    form_class = WorkingPriceForm
    #success_url = reverse_lazy('working_price_list')


class WorkingPriceUpdateView(UpdateView):
    template_name = "WorkingPrice/working_price_form.html"
    model = WorkingPrice
    context_object_name = 'working_price'
    form_class = WorkingPriceForm
    # success_url = reverse_lazy('working_price_list')


class WorkingPriceDeleteView(DeleteView):
    template_name = "WorkingPrice/working_price_confirm_delete.html"
    model = WorkingPrice
    context_object_name = 'working_price'
    success_url = reverse_lazy('working_price_list')
