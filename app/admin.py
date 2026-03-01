from django.contrib import admin
from .models import Topping, Pizza, Proveedor, Cliente, Pedido

admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Pedido)