from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, Subcategoria, Oferta, Plus
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
    productos_plus = Producto.objects.filter(en_plus=True, plus__isnull=False)

    # Verificar si hay suficientes ofertas para obtener 4 elementos aleatorios
    if len(ofertas) >= 4:
        # Obtener 4 ofertas aleatorias
        ofertas_aleatorias = random.sample(list(ofertas), 4)
    else:
        # Si no hay suficientes ofertas, obtén todas las ofertas disponibles
        ofertas_aleatorias = ofertas

    # Filtrar productos en oferta basados en las ofertas aleatorias
    productos_en_oferta = Producto.objects.filter(en_oferta=True, oferta__in=ofertas_aleatorias)

    # Limitar la visualización a 4 productos aleatorios
    productos_en_oferta = random.sample(list(productos_en_oferta), min(4, len(productos_en_oferta)))

    # Resto de tu lógica

    context = {
        'categorias': categorias,
        'productos': productos,
        'productos_en_oferta': productos_en_oferta,
        'ofertas_aleatorias': ofertas_aleatorias,  # Agregar las ofertas aleatorias al contexto si es necesario
        'productos_plus': productos_plus, # Agregar las productos 
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


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    return redirect('lista-productos')  # Redirige a la lista de productos u otra vista deseada.