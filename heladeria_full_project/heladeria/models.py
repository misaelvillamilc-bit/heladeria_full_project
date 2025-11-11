from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("empleado", "Empleado"),
        ("cliente", "Cliente"),
    )
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cliente")

class Ingrediente(models.Model):
    TIPO_CHOICES = (("base","Base"),("complemento","Complemento"),)
    nombre = models.CharField(max_length=150, unique=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    calorias = models.PositiveIntegerField()
    inventario = models.PositiveIntegerField(default=0)
    es_vegetariano = models.BooleanField(default=False)
    es_sano = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    sabor = models.CharField(max_length=100, blank=True, null=True)

    def renovar_inventario(self, cantidad):
        self.inventario = cantidad
        self.save()

    def reducir_a_cero(self):
        self.inventario = 0
        self.save()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_PRODUCTO = (("copa","Copa"),("malteada","Malteada"),)
    nombre = models.CharField(max_length=150, unique=True)
    precio_publico = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    vaso = models.CharField(max_length=100, blank=True, null=True)
    volumen_onzas = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ingredientes = models.ManyToManyField(Ingrediente, through='ProductoIngrediente')

    def costo_produccion(self):
        ingredientes = self.productoingrediente_set.select_related('ingrediente').all()
        total = sum([float(pi.ingrediente.precio) for pi in ingredientes])
        return round(total,2)

    def calorias_totales(self):
        ingredientes = self.productoingrediente_set.select_related('ingrediente').all()
        total = sum([pi.ingrediente.calorias for pi in ingredientes])
        return total

    def rentabilidad(self):
        costo = self.costo_produccion()
        return round(float(self.precio_publico) - float(costo),2)

    def puede_vender(self, cantidad=1):
        ingredientes_rel = self.productoingrediente_set.select_related('ingrediente').all()
        for pi in ingredientes_rel:
            if pi.ingrediente.inventario < cantidad:
                return False
        return True

    def vender(self, usuario, cantidad=1):
        if not self.puede_vender(cantidad):
            raise ValueError('Inventario insuficiente')
        ingredientes_rel = self.productoingrediente_set.select_related('ingrediente').all()
        for pi in ingredientes_rel:
            pi.ingrediente.inventario -= cantidad
            if pi.ingrediente.inventario < 0:
                pi.ingrediente.inventario = 0
            pi.ingrediente.save()
        total = round(float(self.precio_publico) * int(cantidad),2)
        venta = Venta.objects.create(producto=self, usuario=usuario, cantidad=cantidad, total=total)
        return venta

    def __str__(self):
        return self.nombre

class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad_porcion = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    class Meta:
        unique_together = (('producto','ingrediente'),)

    def __str__(self):
        return f"{self.producto.nombre} - {self.ingrediente.nombre}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - {self.producto.nombre} x{self.cantidad}"

# Report helpers
class ReportManager(models.Manager):
    def ventas_por_producto(self):
        from django.db.models import Sum
        return Venta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido')
