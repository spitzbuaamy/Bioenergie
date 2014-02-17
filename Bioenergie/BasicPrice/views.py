from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import BasicPrice, MeasurementPrice, WorkingPrice
from BasicPrice.forms import BasicPriceForm
from django.core.urlresolvers import reverse_lazy


class BasicPriceListView(ListView):
    template_name = "BasicPrice/basic_price_list.html"
    model = BasicPrice
    context_object_name = 'basic_prices'


class BasicPriceDetailView(DetailView):
    template_name = "BasicPrice/basic_price_detail.html"
    model = BasicPrice
    context_object_name = 'basic_price'


class BasicPriceCreateView(CreateView):
    template_name = "BasicPrice/basic_price_form.html"
    model = BasicPrice
    context_object_name = 'basic_price'
    form_class = BasicPriceForm
    #success_url = reverse_lazy('basic_price_list')


class BasicPriceUpdateView(UpdateView):
    template_name = "BasicPrice/basic_price_form.html"
    model = BasicPrice
    context_object_name = 'basic_price'
    form_class = BasicPriceForm
    # success_url = reverse_lazy('bank_list')


class BasicPriceDeleteView(DeleteView):
    template_name = "BasicPrice/basic_price_confirm_delete.html"
    model = BasicPrice
    context_object_name = 'basic_price'
    success_url = reverse_lazy('basic_price_list')


class GroupView(ListView):
    template_name = "group_view.html"
    model = BasicPrice
    model = WorkingPrice
    model = MeasurementPrice
    context_object_name = 'group_views'



