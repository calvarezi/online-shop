from django.shortcuts import render
from .models import Producto, Categoria, Subcategoria, Oferta
from .forms import CustomLoginForm, SignUpForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.db.models import Q
from django.contrib.auth.views import LoginView
import random

def lista_productos(request):
    # Obtener todas las categorías, productos y ofertas
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    ofertas = Oferta.objects.all()

    context = {
        'categorias': categorias,
        'productos': productos,
        'ofertas': ofertas,
    }
    return render(request, 'productos/lista.html', context)

def search_results_view(request):
    template_name = "productos/search_results.html"
    query = request.GET.get('q')
    object_list = Producto.objects.filter(
        Q(nombre__icontains=query) | Q(descripcion__icontains=query)
    )
    context = {
        'object_list': object_list,
    }
    return render(request, template_name, context)

class ProductoDetailView(DetailView):
    model = Producto
    template_name = "productos/detalle.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el producto actual
        producto = self.get_object()
        # Agrega las variables al contexto
        context['producto_imagen_url'] = producto.imagen.url
        context['producto_nombre'] = producto.nombre
        return context

class SignupView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('lista-productos')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'  # Asegúrate de que la ruta sea correcta
    success_url = reverse_lazy('lista-productos')

class ListaOfertasView(ListView):
    model = Producto
    template_name = 'productos/lista_ofertas.html'
    context_object_name = 'productos_en_oferta'

    def get_queryset(self):
        # Obtén todos los productos en oferta
        productos_en_oferta = Producto.objects.filter(en_oferta=True)
        return productos_en_oferta

class CrearOfertaView(CreateView):
    model = Oferta
    template_name = 'productos/crear_oferta.html'
    fields = ['nombre', 'porcentaje_descuento', 'fecha_inicio', 'fecha_finalizacion']
