from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from Abrechnung.models import Bank
from Bank.forms import BankForm
from django.core.urlresolvers import reverse_lazy


class BankListView(ListView):
    template_name = "Bank/bank_list.html"
    model = Bank
    context_object_name = 'banks'


class BankDetailView(DetailView):
    template_name = "Bank/bank_detail.html"
    model = Bank
    context_object_name = 'bank'


class BankCreateView(CreateView):
    template_name = "Bank/bank_form.html"
    model = Bank
    context_object_name = 'bank'
    form_class = BankForm
    #success_url = reverse_lazy('bank_list')


class BankUpdateView(UpdateView):
    template_name = "Bank/bank_form.html"
    model = Bank
    context_object_name = 'bank'
    form_class = BankForm
    # success_url = reverse_lazy('bank_list')


class BankDeleteView(DeleteView):
    template_name = "Bank/bank_confirm_delete.html"
    model = Bank
    context_object_name = 'bank'
    success_url = reverse_lazy('bank_list')