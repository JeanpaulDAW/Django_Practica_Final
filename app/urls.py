from django.urls import path
from . import views

urlpatterns = [
    path("pizzas/", views.pizzas_view, name="pizzas_view"),
    path("toppings/", views.toppings_view, name="toppings_view"),
    path("clientes/", views.clientes_view, name="clientes_view"),
    path("pedidos/", views.pedidos_view, name="pedidos_view"),
]
