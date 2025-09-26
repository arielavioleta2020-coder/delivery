# -*- coding: utf-8 -*-
# poblar_datos.py - Script que preserva restaurantes existentes
import os
import django
import sys

# CONFIGURAR DJANGO PRIMERO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DELIVERI.settings')
django.setup()

from django.contrib.auth.models import User
from restaurantes.models import Restaurante, CategoriaRestaurante

print("✅ Django configurado correctamente")

def crear_datos_preservando_existentes():
    print("🏗️ Agregando datos (preservando existentes)...")
    
    # 1. Crear categorías REALES si no existen
    categorias = [
        {'nombre': 'Pollo Frito', 'icono': '🍗'},
        {'nombre': 'Hamburguesas', 'icono': '🍔'},
        {'nombre': 'Pizza', 'icono': '🍕'}
    ]
    
    for cat_data in categorias:
        if not CategoriaRestaurante.objects.filter(nombre=cat_data['nombre']).exists():
            CategoriaRestaurante.objects.create(**cat_data)
            print(f"✅ Categoría creada: {cat_data['nombre']}")
    
    # 2. Obtener o crear usuario admin
    try:
        usuario = User.objects.get(username='admin')
    except User.DoesNotExist:
        usuario = User.objects.create_user('admin', 'admin@example.com', 'admin123')
        print("✅ Usuario admin creado")
    
    # 3. Obtener categorías
    pollo = CategoriaRestaurante.objects.get(nombre='Pollo Frito')
    hamburguesas = CategoriaRestaurante.objects.get(nombre='Hamburguesas')
    pizza = CategoriaRestaurante.objects.get(nombre='Pizza')
    
    # 4. VERIFICAR restaurantes existentes
    restaurantes_existentes = Restaurante.objects.all()
    print(f"📊 Restaurantes existentes: {restaurantes_existentes.count()}")
    
    # 5. Crear SOLO restaurantes que FALTAN
    restaurantes_a_crear = [
        {
            'nombre': 'KFC',
            'propietario': usuario,
            'categoria': pollo,
            'descripcion': 'El mejor pollo frito de la ciudad',
            'direccion': 'Av. Principal 123, Ciudad',
            'telefono': '555-1001',
            'rating': 4.2,
            'tiempo_entrega': '30-40 min',
            'costo_envio': 2.99,
            'activo': True
        },
        {
            'nombre': 'McDonald\'s',
            'propietario': usuario, 
            'categoria': hamburguesas,
            'descripcion': 'Hamburguesas clásicas y deliciosas',
            'direccion': 'Centro Comercial Mega, Local 45',
            'telefono': '555-1002',
            'rating': 4.0,
            'tiempo_entrega': '20-30 min',
            'costo_envio': 1.99,
            'activo': True
        },
        {
            'nombre': 'Pizza Hut',
            'propietario': usuario,
            'categoria': pizza,
            'descripcion': 'Pizzas frescas y deliciosas',
            'direccion': 'Plaza Central 789, Ciudad',
            'telefono': '555-1003',
            'rating': 4.3,
            'tiempo_entrega': '25-35 min',
            'costo_envio': 2.49,
            'activo': True
        }
    ]
    
    creados = 0
    for datos in restaurantes_a_crear:
        # Verificar si el restaurante YA EXISTE
        if not Restaurante.objects.filter(nombre=datos['nombre']).exists():
            try:
                Restaurante.objects.create(**datos)
                print(f"✅ Restaurante creado: {datos['nombre']}")
                creados += 1
            except Exception as e:
                print(f"❌ Error creando {datos['nombre']}: {e}")
        else:
            print(f"⚠️  Restaurante ya existe: {datos['nombre']}")
    
    print(f"🎉 Proceso completado! Restaurantes nuevos creados: {creados}")
    print(f"📊 Total restaurantes en sistema: {Restaurante.objects.count()}")

if __name__ == '__main__':
    print("=" * 60)
    print("SCRIPT QUE PRESERVA RESTAURANTES EXISTENTES")
    print("=" * 60)
    crear_datos_preservando_existentes()
