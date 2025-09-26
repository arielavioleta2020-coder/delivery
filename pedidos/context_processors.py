from .models import Carrito

def carrito_context(request):
    carrito_count = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
            if carrito:
                carrito_count = carrito.items.count()
        except:
            carrito_count = 0
    return {'carrito_count': carrito_count}