from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Bill
from Bill.forms import BillForm
from django.core.urlresolvers import reverse_lazy


class BillListView(ListView):
    template_name = "Bill/bill_list.html"
    model = Bill
    context_object_name = 'bills'


class BillDetailView(DetailView):
    template_name = "Bill/bill_detail.html"
    model = Bill
    context_object_name = 'bill'


class BillCreateView(CreateView):
    template_name = "Bill/bill_form.html"
    model = Bill
    context_object_name = 'bill'
    form_class = BillForm
    #success_url = reverse_lazy('bill_list')


class BillUpdateView(UpdateView):
    template_name = "Bill/bill_form.html"
    model = Bill
    context_object_name = 'bill'
    form_class = BillForm
    # success_url = reverse_lazy('bill_list')


class BillDeleteView(DeleteView):
    template_name = "Bill/bill_confirm_delete.html"
    model = Bill
    context_object_name = 'bill'
    success_url = reverse_lazy('bill_list')