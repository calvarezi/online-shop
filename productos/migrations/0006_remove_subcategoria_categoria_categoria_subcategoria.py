# Generated by Django 4.0.5 on 2023-07-31 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0005_remove_categoria_categoria_padre_subcategoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategoria',
            name='categoria',
        ),
        migrations.AddField(
            model_name='categoria',
            name='subcategoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='productos.subcategoria'),
            preserve_default=False,
        ),
    ]
