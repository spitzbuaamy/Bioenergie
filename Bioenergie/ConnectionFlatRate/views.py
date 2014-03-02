# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from Abrechnung.models import ConnectionFlatRate
from ConnectionFlatRate.forms import ConnectionFlatRateForm


class ConnectionFlatRateListView(ListView):
    template_name = "ConnectionFlatRate/connection_flat_rate_list.html"
    model = ConnectionFlatRate
    context_object_name = 'connection_flat_rates'


class ConnectionFlatRateDetailView(DetailView):
    template_name = "ConnectionFlatRate/connection_flat_rate_detail.html"
    model = ConnectionFlatRate
    context_object_name = 'connection_flat_rate'


class ConnectionFlatRateCreateView(CreateView):
    template_name = "ConnectionFlatRate/connection_flat_rate_form.html"
    model = ConnectionFlatRate
    context_object_name = 'connection_flat_rate'
    form_class = ConnectionFlatRateForm
    #success_url = reverse_lazy('connection_flat_rate_list')


class ConnectionFlatRateUpdateView(UpdateView):
    template_name = "ConnectionFlatRate/connection_flat_rate_form.html"
    model = ConnectionFlatRate
    context_object_name = 'connection_flat_rate'
    form_class = ConnectionFlatRateForm
    # success_url = reverse_lazy('connection_flat_rate_list')


class ConnectionFlatRateDeleteView(DeleteView):
    template_name = "ConnectionFlatRate/connection_flat_rate_confirm_delete.html"
    model = ConnectionFlatRate
    context_object_name = 'connection_flat_rate'
    success_url = reverse_lazy('connection_flat_rate_list')