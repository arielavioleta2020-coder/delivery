from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Carrito, ItemCarrito  # SOLO importar lo que existe
from restaurantes.models import Producto
from django.http import JsonResponse

@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user, 
        activo=True
    )
    items = ItemCarrito.objects.filter(carrito=carrito)
    total = sum(item.subtotal() for item in items)
    
    return render(request, 'pedidos/carrito.html', {
        'carrito': carrito,
        'items': items,
        'total': total
    })

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user, 
        activo=True
    )
    
    item, item_creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'precio_unitario': producto.precio}
    )
    
    if not item_creado:
        item.cantidad += 1
        item.save()
    
    # Calcular el nuevo conteo del carrito
    carrito_count = ItemCarrito.objects.filter(carrito=carrito).count()
    
    # Devolver JSON para peticiones AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'carrito_count': carrito_count,
            'message': f"'{producto.nombre}' agregado al carrito"
        })
    
    messages.success(request, f"'{producto.nombre}' agregado al carrito")
    return redirect('pedidos:ver_carrito')
    
@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    producto_nombre = item.producto.nombre
    item.delete()
    messages.success(request, f"'{producto_nombre}' eliminado del carrito")
    return redirect('pedidos:ver_carrito')

@login_required
def actualizar_cantidad(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
            messages.success(request, f"Cantidad de '{item.producto.nombre}' actualizada")
        else:
            producto_nombre = item.producto.nombre
            item.delete()
            messages.success(request, f"'{producto_nombre}' eliminado del carrito")
    
    return redirect('pedidos:ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
    items_count = ItemCarrito.objects.filter(carrito=carrito).count()
    
    ItemCarrito.objects.filter(carrito=carrito).delete()
    
    messages.success(request, f"Carrito vaciado. Se eliminaron {items_count} items.")
    return redirect('pedidos:ver_carrito')

# FUNCIÓN SIMPLIFICADA TEMPORALMENTE - SIN Pedido e ItemPedido
@login_required
def crear_pedido_desde_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user, activo=True)
    items_carrito = ItemCarrito.objects.filter(carrito=carrito)
    
    if not items_carrito.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('pedidos:ver_carrito')
    
    total_carrito = sum(item.subtotal() for item in items_carrito)
    
    if request.method == 'POST':
        # VERSIÓN SIMPLIFICADA - solo vacía el carrito
        carrito.activo = False
        carrito.save()
        
        # Crear nuevo carrito vacío
        Carrito.objects.create(usuario=request.user, activo=True)
        
        messages.success(request, f"¡Pedido simulado realizado! Total: ${total_carrito}")
        return redirect('pedidos:ver_carrito')
    
    return render(request, 'pedidos/confirmar_pedido.html', {
        'items': items_carrito,
        'total': total_carrito
    })