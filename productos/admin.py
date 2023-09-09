from django.contrib import admin
from .models import Categoria, Subcategoria, Producto, Oferta

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Producto)
admin.site.register(Oferta)