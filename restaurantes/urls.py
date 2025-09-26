from django.urls import path
from . import views

app_name = 'restaurantes'

urlpatterns = [
    path('', views.lista_restaurantes, name='lista'),
    path('<int:restaurante_id>/', views.detalle_restaurante, name='detalle'),
]