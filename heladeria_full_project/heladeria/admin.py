from django.contrib import admin
from .models import User, Ingrediente, Producto, ProductoIngrediente, Venta

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','rol')

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nombre','tipo','precio','inventario')

class ProductoIngredienteInline(admin.TabularInline):
    model = ProductoIngrediente
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ProductoIngredienteInline]
    list_display = ('nombre','tipo','precio_publico')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto','usuario','cantidad','total','fecha')
