from django.contrib import admin
from .models import CategoriaRestaurante, Restaurante, Producto

admin.site.register(CategoriaRestaurante)
admin.site.register(Restaurante)
admin.site.register(Producto)