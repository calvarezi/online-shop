from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import locale


class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    subcategorias = models.ManyToManyField(Subcategoria)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(
        upload_to='static/img/productos', null=True, blank=True)
    en_oferta = models.BooleanField(default=False)
    oferta = models.ForeignKey('Oferta', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='productos_oferta')
    precio_con_descuento = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    def calcular_precio_con_descuento(self):
        if self.en_oferta and self.oferta:
            # Obtener el porcentaje de descuento de la oferta
            porcentaje_descuento_oferta = self.oferta.porcentaje_descuento

            # Calcular el precio con descuento
            precio_con_descuento = self.precio_original - \
                (self.precio_original * porcentaje_descuento_oferta / 100)

            return precio_con_descuento
        else:
            return self.precio_original

    def precio_original_formateado(self):
        return locale.format_string("%.0f", self.precio_original, grouping=True)

    def precio_con_descuento_formateado(self):
        if self.precio_con_descuento is not None:
            return locale.format_string("%.0f", self.precio_con_descuento, grouping=True)
        else:
            return None

    def save(self, *args, **kwargs):
        self.precio_con_descuento = self.calcular_precio_con_descuento()
        self.slug = slugify(self.nombre)
        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Oferta(models.Model):
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    nombre = models.CharField(max_length=100)  # Agrega este campo

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Oferta, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


@receiver(post_save, sender=Oferta)
def actualizar_precios_con_descuento(sender, instance, **kwargs):
    # Recalcula los precios con descuento para todos los productos relacionados a la oferta
    productos_afectados = Producto.objects.filter(oferta=instance)
    for producto in productos_afectados:
        producto.save()
