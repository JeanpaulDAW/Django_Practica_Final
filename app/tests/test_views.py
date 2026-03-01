# -*- coding: utf-8 -*-
import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from app.models import Pizza, Topping, Proveedor

# --- CONFIGURACIÓN OBLIGATORIA ---
# El alumno debe poner aquí su usuario de GitHub o un identificador único.
# Esto es fundamental para que los datos de prueba generados sean únicos.
GITHUB_USERNAME = "JeanpaulDAW"  # <-- SUSTITUIR POR TU USUARIO DE GITHUB


class PracticaTestBase(TestCase):
    """
    Clase base para los tests de la práctica.
    Se encarga de generar datos de prueba únicos usando Faker y una semilla.
    """

    def setUp(self):
        """
        Configuración inicial que se ejecuta antes de cada test.
        """
        self.faker = self.generar_datos_de_prueba()
        self.cliente_api = self.client

        # --- Creación de datos de referencia para usar en los tests ---
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Test", email="test@proveedor.com"
        )
        self.topping = Topping.objects.create(nombre="Queso Test", es_vegetariano=True)
        self.pizza = Pizza.objects.create(nombre="Pizza Test", precio=Decimal("9.99"))
        self.pizza.toppings.add(self.topping)

    def generar_datos_de_prueba(self):
        """
        Genera una instancia de Faker con una semilla basada en GITHUB_USERNAME.
        Esto asegura que los datos generados sean consistentes entre ejecuciones.
        """
        if GITHUB_USERNAME == "tu_usuario_aqui":
            raise ValueError(
                "Es obligatorio modificar la variable GITHUB_USERNAME en "
                "'app/tests/test_views.py' "
                "con tu nombre de usuario de GitHub para continuar."
            )
        Faker.seed(GITHUB_USERNAME)
        return Faker("es_ES")


class PracticaViewsTests(PracticaTestBase):
    """
    Suite de tests para las vistas (API) del sistema.
    Los tests de Topping, Proveedor y Pizza sirven como REFERENCIA.
    Debes implementar la lógica de los tests de Cliente y
    Pedido siguiendo los docstrings.
    """

    # --- TESTS DE REFERENCIA (PIZZAS) ---

    def test_referencia_listar_pizzas_ok(self):
        """Referencia: Verifica que GET /pizzas/ devuelve una lista."""
        response = self.cliente_api.get(reverse("pizzas_view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("pizzas", response.json())
        self.assertEqual(len(response.json()["pizzas"]), 1)

    def test_referencia_crear_pizza_ok(self):
        """Referencia: Verifica que POST /pizzas/ crea una pizza con toppings."""
        data = {
            "nombre": "Pizza Nueva",
            "precio": "15.50",
            "toppings": [self.topping.id],
        }
        response = self.cliente_api.post(
            reverse("pizzas_view"), json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Pizza.objects.filter(nombre="Pizza Nueva").exists())
        nueva_pizza = Pizza.objects.get(nombre="Pizza Nueva")
        self.assertIn(self.topping, nueva_pizza.toppings.all())

    def test_referencia_crear_pizza_sin_precio_falla(self):
        """Referencia: Verifica que POST /pizzas/ sin precio da error 400."""
        data = {"nombre": "Pizza Incompleta"}
        response = self.cliente_api.post(
            path=reverse("pizzas_view"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_referencia_crear_pizza_toppings_inexistentes_falla(self):
        """Referencia: Verifica que POST /pizzas/ con toppings inexistentes 
        da error 400."""
        data = {
            "nombre": "Pizza Fallida",
            "precio": "10.00",
            "toppings": [99999],  # ID inexistente
        }
        response = self.cliente_api.post(
            path=reverse("pizzas_view"),
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    # --- TESTS PARA CLASE (TOPPINGS) ---

    def test_referencia_listar_toppings_ok(self):
        """Referencia: Verifica que GET /toppings/ devuelve una lista."""
        pass

    def test_referencia_crear_topping_ok(self):
        """Referencia: Verifica que POST /toppings/ crea un topping."""
        pass

    def test_referencia_crear_topping_sin_nombre_falla(self):
        """Referencia: Verifica que POST /toppings/ sin nombre da error 400."""
        pass

    # --- TESTS PARA IMPLEMENTAR (CLIENTES) ---

    def test_crear_cliente_ok(self):
        """
        [TAREA - 1.0 PUNTOS]
        Verifica que se puede crear un cliente nuevo mediante una petición POST
        a /clientes/.
        - La petición debe enviar 'nombre', 'email' y 'telefono'.
        - El código de respuesta esperado es 201 (Created).
        - El cliente debe existir en la base de datos después de la petición.
        """
        pass

    def test_crear_cliente_email_duplicado_falla(self):
        """
        [TAREA - 1.0 PUNTOS]
        Verifica que la API no permite crear un cliente con un email que ya existe.
        - Primero crea un cliente en la base de datos (usando Cliente.objects.create).
        - Luego intenta crear otro cliente mediante la API usando el mismo email.
        - El código de respuesta esperado es 400 (Bad Request).
        """
        pass

    def test_listar_clientes_ok(self):
        """
        [TAREA - 0.5 PUNTOS]
        Verifica que se puede obtener la lista de clientes mediante GET a /clientes/.
        - El código de respuesta esperado es 200 (OK).
        - La respuesta JSON debe contener una clave 'clientes', que sea una lista.
        - La lista debe contener al menos un cliente.
        """
        pass

    # --- TESTS PARA IMPLEMENTAR (PEDIDOS) ---

    def test_crear_pedido_ok(self):
        """
        [TAREA - 1.5 PUNTOS]
        Verifica que se puede crear un pedido nuevo mediante POST a /pedidos/.
        - La petición debe enviar 'cliente' (ID), 'direccion_entrega' y 'pizzas'.
        - El código de respuesta esperado es 201 (Created).
        - El JSON de respuesta debe contener el total calculado del pedido.
        - El pedido debe existir en la base de datos con las pizzas asociadas.
        """
        pass

    def test_crear_pedido_cliente_inexistente_falla(self):
        """
        [TAREA - 1.0 PUNTOS]
        Verifica que no se puede crear un pedido si el ID del cliente no existe.
        - Envía un ID de cliente que no exista en la base de datos (p. ej., 9999).
        - El código de respuesta esperado es 400 (Bad Request).
        """
        pass

    def test_crear_pedido_pizzas_inexistentes_falla(self):
        """
        [TAREA - 0.5 PUNTOS]
        Verifica que no se puede crear un pedido si alguna de las pizzas no existe.
        - Envía una lista de pizzas donde al menos una ID no exista (p. ej., [9999]).
        - El código de respuesta esperado es 400 (Bad Request).
        """
        pass

    def test_listar_pedidos_ok(self):
        """
        [TAREA - 0.5 PUNTOS]
        Verifica que se puede obtener la lista de pedidos mediante GET a /pedidos/.
        - Crea primero un pedido para asegurar que la lista no esté vacía.
        - El código de respuesta esperado es 200 (OK).
        - La respuesta JSON debe contener una clave 'pedidos'.
        - Cada pedido en la lista debe incluir detalles del cliente y de las pizzas.
        """
        pass
