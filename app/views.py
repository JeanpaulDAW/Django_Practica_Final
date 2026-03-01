from django.http import JsonResponse
from .models import Cliente, Pedido, Pizza, Topping
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json


@csrf_exempt
def pizzas_view(request):
    if request.method == "GET":
        pizzas = Pizza.objects.all()
        data = []
        for pizza in pizzas:
            toppings_data = []
            for t in pizza.toppings.all():
                toppings_data.append({"id": t.id, "nombre": t.nombre})
            data.append(
                {
                    "id": pizza.id,
                    "nombre": pizza.nombre,
                    "precio": str(pizza.precio),
                    "toppings": toppings_data,
                }
            )
        return JsonResponse({"pizzas": data})

    if request.method == "POST":
        data = json.loads(request.body)

        nombre = data.get("nombre")
        precio = data.get("precio")
        topping_ids = data.get("toppings", [])

        if not nombre or not precio:
            return JsonResponse(
                {"error": "Los campos 'nombre' y 'precio' son obligatorios"}, status=400
            )

        # Validación robusta: Verificar que todos los toppings existen
        if topping_ids:
            # Filtramos los toppings que coinciden con los IDs recibidos
            toppings_existentes = Topping.objects.filter(id__in=topping_ids).count()
            if toppings_existentes != len(topping_ids):
                return JsonResponse(
                    {"error": "Uno o más toppings no existen"}, status=400
                )

        pizza = Pizza.objects.create(nombre=nombre, precio=precio)

        if topping_ids:
            pizza.toppings.set(topping_ids)

        return JsonResponse(
            {
                "id": pizza.id,
                "nombre": pizza.nombre,
                "precio": str(pizza.precio),
                "toppings": [t.id for t in pizza.toppings.all()],
            },
            status=201,
        )


    return JsonResponse({"error": "Método no soportado"}, status=405)


@csrf_exempt
def toppings_view(request):

    if request.method == "GET":
        toppings = Topping.objects.all()

        data = []
        for topping in toppings:
            data.append({
                "id": topping.id,
                "nombre": topping.nombre,
                "es_vegetariano": topping.es_vegetariano
            })

        return JsonResponse(data, safe=False, status=200)


    if request.method == "POST":
        data = json.loads(request.body)

        nombre = data.get("nombre")
        es_vegetariano = data.get("es_vegetariano")

        if not nombre or es_vegetariano is None:
            return JsonResponse(
                {"error": "Los campos 'nombre' y 'es_vegetariano' son obligatorios"},
                status=400
            )

        topping = Topping.objects.create(
            nombre=nombre,
            es_vegetariano=es_vegetariano
        )

        return JsonResponse(
            {
                "id": topping.id,
                "nombre": topping.nombre,
                "es_vegetariano": topping.es_vegetariano
            },
            status=201
        )

    return JsonResponse(
        {"error": "Método no soportado"},
        status=405
    )


@csrf_exempt
def clientes_view(request):
    if request.method == "GET":
        clientes = Cliente.objects.all()
        data = [model_to_dict(cliente) for cliente in clientes]
        return JsonResponse(data, safe=False, status=200)

    if request.method == "POST":
        try:
            body = json.loads(request.body)

            cliente = Cliente.objects.create(
                nombre=body["nombre"],
                email=body["email"],
                telefono=body.get("telefono", "")
            )

            return JsonResponse(
                model_to_dict(cliente),
                status=201
            )

        except Exception:
            return JsonResponse(
                {"error": "Datos inválidos"},
                status=400
            )

@csrf_exempt
def pedidos_view(request):
    if request.method == "GET":
        pedidos = Pedido.objects.all()
        data = []

        for pedido in pedidos:
            pedido_dict = model_to_dict(pedido)
            pedido_dict["pizzas"] = list(
                pedido.pizzas.values_list("id", flat=True)
            )
            pedido_dict["total"] = str(pedido.calcular_total())
            data.append(pedido_dict)

        return JsonResponse(data, safe=False, status=200)

    if request.method == "POST":
        try:
            body = json.loads(request.body)

            cliente = Cliente.objects.get(id=body["cliente"])
            pedido = Pedido.objects.create(
                cliente=cliente,
                direccion_entrega=body["direccion_entrega"]
            )

            pizzas = Pizza.objects.filter(id__in=body["pizzas"])
            pedido.pizzas.set(pizzas)

            pedido_dict = model_to_dict(pedido)
            pedido_dict["pizzas"] = list(
                pedido.pizzas.values_list("id", flat=True)
            )
            pedido_dict["total"] = str(pedido.calcular_total())

            return JsonResponse(pedido_dict, status=201)

        except Exception:
            return JsonResponse(
                {"error": "Datos inválidos"},
                status=400
            )