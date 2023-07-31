# Generated by Django 4.0.5 on 2023-07-31 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_remove_subcategoria_categoria_categoria_subcategoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='subcategoria',
        ),
        migrations.AddField(
            model_name='categoria',
            name='subcategorias',
            field=models.ManyToManyField(to='productos.subcategoria'),
        ),
    ]
