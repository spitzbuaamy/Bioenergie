from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from Abrechnung.models import Index, Customer, Building
from Index.forms import IndexForm
from django.core.urlresolvers import reverse_lazy


class IndexListView(ListView):
    template_name = "Index/index_list.html"
    model = Index
    context_object_name = 'indexes'


class IndexDetailView(DetailView):
    template_name = "Index/index_detail.html"
    model = Index
    context_object_name = 'index'


class IndexCreateView(CreateView):
    template_name = "Index/index_form.html"
    model = Index
    context_object_name = 'index'
    form_class = IndexForm
    #success_url = reverse_lazy('index_list')


class IndexUpdateView(UpdateView):
    template_name = "Index/index_form.html"
    model = Index
    context_object_name = 'index'
    form_class = IndexForm
    # success_url = reverse_lazy('index_list')


class IndexDeleteView(DeleteView):
    template_name = "Index/index_confirm_delete.html"
    model = Index
    context_object_name = 'index'
    success_url = reverse_lazy('index_list')
