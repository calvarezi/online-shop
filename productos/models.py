from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
import locale
from django.db.models.signals import pre_delete
from django.utils.html import escape

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
    nombre = models.CharField(max_length=20)
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
    en_plus = models.BooleanField(default=False)
    plus = models.ForeignKey('Plus', on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_plus')
    precio_con_descuento_plus = models.DecimalField(
    max_digits=10, decimal_places=2, blank=True, null=True)


    def precio_original_formateado(self):
        return locale.format_string("%.0f", self.precio_original, grouping=True)

    def precio_con_descuento_formateado(self):
        if self.precio_con_descuento is not None:
            return locale.format_string("%.0f", self.precio_con_descuento, grouping=True)
        else:
            return None
        
    def save(self, *args, **kwargs):
        self.precio_con_descuento = calcular_precio_con_descuento(self)
        self.precio_con_descuento_plus = calcular_precio_plus(self)
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
        producto.precio_con_descuento = calcular_precio_con_descuento(producto)
        producto.save()

class Plus(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='plus_producto')
    oferta_relacionada = models.ForeignKey('Oferta', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_finalizacion = models.DateField()
    nombre = models.CharField(max_length=100)

    def calcular_porcentaje_descuento(self):
        # Obtén el porcentaje de descuento de la oferta relacionada
        porcentaje_descuento_oferta = self.oferta_relacionada.porcentaje_descuento

        # Asigna el mismo porcentaje de descuento al Plus
        self.porcentaje_descuento = porcentaje_descuento_oferta

    def save(self, *args, **kwargs):
        # Calcula y asigna el porcentaje de descuento al guardar
        self.calcular_porcentaje_descuento()
        super(Plus, self).save(*args, **kwargs)

    def __str__(self):
        return f"Plus para {self.producto.nombre}"

@receiver(pre_delete, sender=Producto)
def eliminar_imagen_producto(sender, instance, **kwargs):
    # Borra la imagen asociada al producto al eliminar el producto
    if instance.imagen:
        instance.imagen.delete(save=False)


def calcular_precio_con_descuento(producto):
    if producto.en_oferta and producto.oferta:
        # Obtener el porcentaje de descuento de la oferta
        porcentaje_descuento_oferta = producto.oferta.porcentaje_descuento

        # Calcular el precio con descuento
        precio_con_descuento = producto.precio_original - \
            (producto.precio_original * porcentaje_descuento_oferta / 100)

        return precio_con_descuento
    else:
        return producto.precio_original

def calcular_precio_plus(producto):
    if producto.en_plus and producto.oferta:
        porcentaje_descuento_oferta = producto.oferta.porcentaje_descuento
        precio_con_descuento_plus = producto.precio_original - (producto.precio_original * porcentaje_descuento_oferta / 100)
        return precio_con_descuento_plus
    else:
        return producto.precio_original