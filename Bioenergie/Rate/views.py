from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import Rate
from Rate.forms import RateForm


class RateListView(ListView):
    template_name = "Rate/rate_list.html"
    model = Rate
    context_object_name = 'rates'


class RateDetailView(DetailView):
    template_name = "Rate/rate_detail.html"
    model = Rate
    context_object_name = 'rate'


class RateCreateView(CreateView):
    template_name = "Rate/rate_form.html"
    model = Rate
    context_object_name = 'rate'
    form_class = RateForm
    #success_url = reverse_lazy('rate_list')


class RateUpdateView(UpdateView):
    template_name = "Rate/rate_form.html"
    model = Rate
    context_object_name = 'rate'
    form_class = RateForm
    # success_url = reverse_lazy('rate_list')


class RateDeleteView(DeleteView):
    template_name = "Rate/rate_confirm_delete.html"
    model = Rate
    context_object_name = 'rate'
    success_url = reverse_lazy('rate_list')
