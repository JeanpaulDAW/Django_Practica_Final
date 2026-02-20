from django.http import JsonResponse
from .models import Pizza, Topping
from django.views.decorators.csrf import csrf_exempt
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
