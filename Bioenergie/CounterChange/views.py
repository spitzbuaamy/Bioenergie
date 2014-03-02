from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import CounterChange
from CounterChange.forms import CounterChangeForm
from django.core.urlresolvers import reverse_lazy


class CounterChangeListView(ListView):
    template_name = "CounterChange/counter_change_list.html"
    model = CounterChange
    context_object_name = 'counter_changes'


class CounterChangeDetailView(DetailView):
    template_name = "CounterChange/counter_change_detail.html"
    model = CounterChange
    context_object_name = 'counter_change'


class CounterChangeCreateView(CreateView):
    template_name = "CounterChange/counter_change_form.html"
    model = CounterChange
    context_object_name = 'counter_change'
    form_class = CounterChangeForm
    #success_url = reverse_lazy('counter_change_list')

    def get_form(self, form_class):
        form = super(CounterChangeCreateView,self).get_form(form_class)
        form.fields['date'].widget.attrs.update({'class': 'datepicker'})
        form.fields['date_new_counter'].widget.attrs.update({"class": "datepicker"})
        return form


class CounterChangeUpdateView(UpdateView):
    template_name = "CounterChange/counter_change_form.html"
    model = CounterChange
    context_object_name = 'counter_change'
    form_class = CounterChangeForm
    # success_url = reverse_lazy('counter_change_list')

    def get_form(self, form_class):
        form = super(CounterChangeUpdateView,self).get_form(form_class)
        form.fields['date'].widget.attrs.update({'class': 'datepicker'})
        form.fields['date_new_counter'].widget.attrs.update({"class": "datepicker"})
        return form

class CounterChangeDeleteView(DeleteView):
    template_name = "CounterChange/counter_change_confirm_delete.html"
    model = CounterChange
    context_object_name = 'counter_change'
    success_url = reverse_lazy('counter_change_list')