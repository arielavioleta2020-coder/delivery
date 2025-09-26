# agregar_productos_seguro.py - SOLO AGREGA, NO TOCA EXISTENTES
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DELIVERI.settings')
django.setup()

from restaurantes.models import Restaurante, CategoriaRestaurante, Producto
from django.contrib.auth.models import User

print("➕ AGREGANDO PRODUCTOS Y SUSHI EXPRESS")

# Obtener usuario admin
usuario = User.objects.get(username='admin')

# 1. PRIMERO: Agregar Sushi Express si no existe
if not Restaurante.objects.filter(nombre='Sushi Express').exists():
    # Crear categoría Asiática si no existe
    categoria_asiatica, created = CategoriaRestaurante.objects.get_or_create(
        nombre='Asiática',
        defaults={'icono': '🍣'}
    )
    
    sushi_express = Restaurante.objects.create(
        nombre='Sushi Express',
        propietario=usuario,
        categoria=categoria_asiatica,
        descripcion='Sushi fresco y delicioso preparado por chefs expertos',
        direccion='Avenida Oriental 567, Ciudad',
        telefono='555-4001',
        rating=4.7,
        tiempo_entrega='30-40 min',
        costo_envio=3.50,
        activo=True
    )
    print("✅ Sushi Express creado")
    
    # Productos para Sushi Express
    productos_sushi = [
        {'nombre': 'Combo Sushi Mixto', 'precio': 22.99, 'descripcion': '20 piezas de sushi variado'},
        {'nombre': 'Ramen Tradicional', 'precio': 12.99, 'descripcion': 'Ramen con cerdo y vegetales'},
        {'nombre': 'Tempura de Camarón', 'precio': 15.99, 'descripcion': '8 piezas de tempura crujiente'},
        {'nombre': 'Sashimi de Salmón', 'precio': 18.99, 'descripcion': '10 piezas de sashimi fresco'},
        {'nombre': 'Bowl de Poke', 'precio': 14.99, 'descripcion': 'Bowl con salmón, aguacate y arroz'},
    ]
    
    for prod in productos_sushi:
        if not Producto.objects.filter(restaurante=sushi_express, nombre=prod['nombre']).exists():
            Producto.objects.create(restaurante=sushi_express, **prod, disponible=True)
            print(f"✅ Producto agregado a Sushi Express: {prod['nombre']}")

# 2. SEGUNDO: Agregar productos a los restaurantes existentes

# Productos para KFC
kfc = Restaurante.objects.get(nombre='KFC')
productos_kfc = [
    {'nombre': 'Bucket Familiar', 'precio': 24.99, 'descripcion': '8 piezas de pollo + papas + ensalada'},
    {'nombre': 'Combo Individual', 'precio': 8.99, 'descripcion': '2 piezas de pollo + papas + bebida'},
    {'nombre': 'Alitas Picantes', 'precio': 12.99, 'descripcion': '10 alitas bañadas en salsa picante'},
]

for prod in productos_kfc:
    if not Producto.objects.filter(restaurante=kfc, nombre=prod['nombre']).exists():
        Producto.objects.create(restaurante=kfc, **prod, disponible=True)
        print(f"✅ Producto agregado a KFC: {prod['nombre']}")

# Productos para McDonald's
mcdonalds = Restaurante.objects.get(nombre="McDonald's")
productos_mcdonalds = [
    {'nombre': 'Big Mac Menu', 'precio': 7.99, 'descripcion': 'Big Mac + papas + bebida'},
    {'nombre': 'McNuggets 10 piezas', 'precio': 5.99, 'descripcion': '10 nuggets + salsa'},
    {'nombre': 'Cuarto de Libra', 'precio': 6.99, 'descripcion': 'Hamburguesa con queso y bacon'},
]

for prod in productos_mcdonalds:
    if not Producto.objects.filter(restaurante=mcdonalds, nombre=prod['nombre']).exists():
        Producto.objects.create(restaurante=mcdonalds, **prod, disponible=True)
        print(f"✅ Producto agregado a McDonald's: {prod['nombre']}")

# Productos para Pizza Hut
pizza_hut = Restaurante.objects.get(nombre='Pizza Hut')
productos_pizza_hut = [
    {'nombre': 'Pizza Grande', 'precio': 18.99, 'descripcion': 'Pizza familiar 3 ingredientes'},
    {'nombre': 'Pizza Mediana', 'precio': 14.99, 'descripcion': 'Pizza mediana 2 ingredientes'},
    {'nombre': 'Palitos de Ajo', 'precio': 8.99, 'descripcion': '8 palitos de ajo con salsa'},
]

for prod in productos_pizza_hut:
    if not Producto.objects.filter(restaurante=pizza_hut, nombre=prod['nombre']).exists():
        Producto.objects.create(restaurante=pizza_hut, **prod, disponible=True)
        print(f"✅ Producto agregado a Pizza Hut: {prod['nombre']}")

print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
print(f"📊 Restaurantes totales: {Restaurante.objects.count()}")
print(f"📊 Productos totales: {Producto.objects.count()}")
