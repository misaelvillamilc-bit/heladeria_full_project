from django import forms
from .models import Ingrediente, Producto

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','precio_publico','tipo','vaso','volumen_onzas']
