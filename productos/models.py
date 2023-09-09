from django.db import models
from django.utils.text import slugify


# Create your models here.

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    subcategorias = models.ManyToManyField(Subcategoria)

    def __str__(self):
        return self.nombre


class Oferta(models.Model):
    producto = models.OneToOneField('Producto', on_delete=models.CASCADE, related_name='oferta_producto')
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Oferta para {self.producto.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(
        upload_to='static/img/productos', null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    oferta = models.OneToOneField(Oferta, null=True, blank=True, on_delete=models.SET_NULL, related_name= 'oferta_producto')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']