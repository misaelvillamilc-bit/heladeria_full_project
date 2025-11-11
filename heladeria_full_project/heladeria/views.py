from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Ingrediente, Venta
from .forms import IngredienteForm, ProductoForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})

@login_required
def vender_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    try:
        venta = producto.vender(request.user, cantidad=1)
        return redirect('index')
    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})

@login_required
def ingredientes_crud(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredientes')
    else:
        form = IngredienteForm()
    ingredientes = Ingrediente.objects.all()
    return render(request, 'ingredientes.html', {'ingredientes': ingredientes,'form': form})

@login_required
def productos_crud(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos,'form': form})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})
