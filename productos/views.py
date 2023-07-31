from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Producto
from django.views.generic.detail import DetailView
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views.generic import CreateView




class ProductListView(ListView):
    model = Producto
    template_name = 'productos/lista.html'


class SearchResultsView(ListView):

    model = Producto
    template_name = "productos/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Producto.objects.filter(
            Q(nombre__icontains=query) | Q(descripción__icontains=query)
        )
        return object_list
    

class ProductoDetailView(DetailView):
  model = Producto
  template_name = "productos/detalle.html"


class SignupView(CreateView):
  form_class = SignUpForm
  success_url = reverse_lazy('lista-productos')
  template_name = 'registration/signup.html'