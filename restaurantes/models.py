from django.db import models
from django.contrib.auth.models import User

class CategoriaRestaurante(models.Model):
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, default='🍽️')
    
    def __str__(self):
        return self.nombre

class Restaurante(models.Model):
    nombre = models.CharField(max_length=200)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaRestaurante, on_delete=models.CASCADE)
    descripcion = models.TextField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    imagen = models.ImageField(upload_to='restaurantes/', default='restaurantes/default.jpg')
    rating = models.FloatField(default=0)
    tiempo_entrega = models.CharField(max_length=20, default='30-40 min')
    costo_envio = models.DecimalField(max_digits=6, decimal_places=2, default=2.99)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', default='productos/default.jpg')
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.restaurante.nombre}"