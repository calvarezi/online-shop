from django.shortcuts import render
from .models import Producto, Categoria, Subcategoria, Oferta
from django.views.generic.detail import DetailView
from .forms import CustomLoginForm, SignUpForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.utils import timezone





def lista_productos(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    context = {
        'categorias': categorias,
        'productos': productos
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


class SignupView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('lista-productos')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'  # Asegúrate de que la ruta sea correcta
    success_url = reverse_lazy('lista-productos')



def lista_ofertas(request):
    ofertas = Oferta.objects.filter(fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now())
    return render(request, 'lista_ofertas.html', {'ofertas': ofertas})