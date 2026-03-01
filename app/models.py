from django.db import models
from decimal import Decimal


class Topping(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    es_vegetariano = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# Constante para los estados de la Pizza
ESTADOS_PIZZA = [
    ("DIS", "Disponible"),
    ("PRO", "Promoción"),
    ("PRG", "Programada"),
    ("CAN", "Cancelada"),
]


class Pizza(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_fabricacion = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=3,
        choices=ESTADOS_PIZZA,
        default="DIS",
    )
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True, help_text="Email contacto proveedor.")
    telefono = models.CharField(max_length=20, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_alta = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    pizzas = models.ManyToManyField("Pizza", related_name="pedidos")
    direccion_entrega = models.CharField(max_length=255)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default="Pendiente")

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.nombre}"

    def calcular_total(self):
        total = Decimal("0.00")
        for pizza in self.pizzas.all():
            total += pizza.precio
        return total