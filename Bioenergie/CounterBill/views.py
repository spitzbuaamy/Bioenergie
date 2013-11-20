from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import CounterBill
from CounterBill.forms import CounterBillForm
from django.core.urlresolvers import reverse_lazy


class CounterBillListView(ListView):
    template_name = "CounterBill/counter_bill_list.html"
    model = CounterBill
    context_object_name = 'counter_bills'


class CounterBillDetailView(DetailView):
    template_name = "CounterBill/counter_bill_detail.html"
    model = CounterBill
    context_object_name = 'counter_bill'


class CounterBillCreateView(CreateView):
    template_name = "CounterBill/counter_bill_form.html"
    model = CounterBill
    context_object_name = 'counter_bill'
    form_class = CounterBillForm
    #success_url = reverse_lazy('counter_bill_list')


class CounterBillUpdateView(UpdateView):
    template_name = "CounterBill/counter_bill_form.html"
    model = CounterBill
    context_object_name = 'counter_bill'
    form_class = CounterBillForm
    # success_url = reverse_lazy('counter_bill_list')


class CounterBillDeleteView(DeleteView):
    template_name = "CounterBill/counter_bill_confirm_delete.html"
    model = CounterBill
    context_object_name = 'counter_bill'
    success_url = reverse_lazy('counter_bill_list')