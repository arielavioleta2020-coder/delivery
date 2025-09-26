from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

# Intentar importar los modelos, si no existen usar datos de ejemplo
try:
    from .models import Restaurante, Producto
    MODELOS_DISPONIBLES = True
except:
    MODELOS_DISPONIBLES = False

# Datos de ejemplo (solo si no hay modelos)
if not MODELOS_DISPONIBLES:
    RESTAURANTES_EJEMPLO = [
    {
        'id': 1,
        'nombre': 'KFC',
        'categoria': 'Pollo Frito',
        'descripcion': 'El mejor pollo frito de la ciudad',
        'rating': 4.2,
        'tiempo_entrega': '30-40 min',
        'costo_envio': 2.99,
        'imagen': 'https://images.unsplash.com/photo-1626645735466-5f4fe9121e2b?ixlib=rb-4.0.3&w=400'
    },
    {
        'id': 2,
        'nombre': 'McDonald\'s',
        'categoria': 'Hamburguesas',
        'descripcion': 'Hamburguesas clásicas y deliciosas',
        'rating': 4.0,
        'tiempo_entrega': '20-30 min',
        'costo_envio': 1.99,
        'imagen': 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?ixlib=rb-4.0.3&w=400'
    },
    {
        'id': 3,
        'nombre': 'Pizza Hut',
        'categoria': 'Pizza',
        'descripcion': 'Pizzas frescas y deliciosas',
        'rating': 4.3,
        'tiempo_entrega': '25-35 min',
        'costo_envio': 2.49,
        'imagen': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-4.0.3&w=400'
    }
]

PRODUCTOS_EJEMPLO = {
    1: [  # KFC
        {'nombre': 'Bucket Familiar', 'precio': 24.99, 'descripcion': '8 piezas de pollo + papas + ensalada'},
        {'nombre': 'Combo Individual', 'precio': 8.99, 'descripcion': '2 piezas de pollo + papas + bebida'},
    ],
    2: [  # McDonald's
        {'nombre': 'Big Mac Menu', 'precio': 7.99, 'descripcion': 'Big Mac + papas + bebida'},
        {'nombre': 'McNuggets 10 piezas', 'precio': 5.99, 'descripcion': '10 nuggets + salsa'},
    ],
    3: [  # Pizza Hut
        {'nombre': 'Pizza Grande', 'precio': 18.99, 'descripcion': 'Pizza familiar 3 ingredientes'},
        {'nombre': 'Pizza Mediana', 'precio': 14.99, 'descripcion': 'Pizza mediana 2 ingredientes'},
    ]
}

@login_required
def lista_restaurantes(request):
    if MODELOS_DISPONIBLES:
        # Usar base de datos real
        restaurantes = Restaurante.objects.all()
        context = {
            'restaurantes': restaurantes,
            'categorias': ['Pollo', 'Hamburguesas', 'Pizza', 'Sushi', 'Mexicana', 'China', 'Italiana']
        }
    else:
        # Usar datos de ejemplo
        context = {
            'restaurantes': RESTAURANTES_EJEMPLO,
            'categorias': ['Pollo', 'Hamburguesas', 'Pizza', 'Sushi', 'Mexicana']
        }
    
    return render(request, 'restaurantes/lista.html', context)

@login_required
def detalle_restaurante(request, restaurante_id):
    if MODELOS_DISPONIBLES:
        # Usar base de datos real
        restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        productos = Producto.objects.filter(restaurante=restaurante)
        
        context = {
            'restaurante': restaurante,
            'productos': productos
        }
    else:
        # Usar datos de ejemplo
        restaurante = next((r for r in RESTAURANTES_EJEMPLO if r['id'] == restaurante_id), None)
        
        if not restaurante:
            return render(request, 'restaurantes/error.html', {'mensaje': 'Restaurante no encontrado'})
        
        productos = PRODUCTOS_EJEMPLO.get(restaurante_id, [])
        
        context = {
            'restaurante': restaurante,
            'productos': productos
        }
    
    return render(request, 'restaurantes/detalle.html', context)