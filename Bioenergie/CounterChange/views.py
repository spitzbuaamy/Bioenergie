from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Counter
from CounterChange.forms import CounterForm
from django.core.urlresolvers import reverse_lazy


class CounterListView(ListView):
    template_name = "Counter/counter_list.html"
    model = Counter
    context_object_name = 'counters'


class CounterDetailView(DetailView):
    template_name = "Counter/counter_detail.html"
    model = Counter
    context_object_name = 'counter'


class CounterCreateView(CreateView):
    template_name = "Counter/counter_form.html"
    model = Counter
    context_object_name = 'counter'
    form_class = CounterForm
    #success_url = reverse_lazy('counter_list')


class CounterUpdateView(UpdateView):
    template_name = "Counter/counter_form.html"
    model = Counter
    context_object_name = 'counter'
    form_class = CounterForm
    # success_url = reverse_lazy('counter_list')


class CounterDeleteView(DeleteView):
    template_name = "Counter/counter_confirm_delete.html"
    model = Counter
    context_object_name = 'counter'
    success_url = reverse_lazy('counter_list')
