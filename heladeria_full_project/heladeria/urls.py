from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('vender/<int:pk>/', views.vender_producto, name='vender_producto'),
    path('ingredientes/', views.ingredientes_crud, name='ingredientes'),
    path('productos/', views.productos_crud, name='productos'),
    path('registro/', views.registro, name='registro'),
]
