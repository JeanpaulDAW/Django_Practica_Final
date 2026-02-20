# -*- coding: utf-8 -*-
from decimal import Decimal
from django.test import TestCase
from app.models import Pizza, Topping, Proveedor
# from app.models import Cliente, Pedido  # DESCOMENTAR CUANDO CREES LOS MODELOS


class PracticaModelsTests(TestCase):
    """
    Suite de tests para los modelos del sistema.
    Los tests de Topping, Proveedor y Pizza sirven como REFERENCIA.
    Debes implementar la lógica de los tests de Cliente
    y Pedido siguiendo los docstrings.
    """

    def setUp(self):
        """
        Configuración inicial para los tests.
        Crea instancias de los modelos de referencia y de los que se van a probar.
        """
        # --- DATOS DE REFERENCIA (VISTOS EN CLASE) ---
        self.topping = Topping.objects.create(nombre="Extra Queso", es_vegetariano=True)
        self.proveedor = Proveedor.objects.create(
            nombre="Proveedor Central", email="central@pizzas.com"
        )
        self.pizza_1 = Pizza.objects.create(nombre="Margarita", precio=Decimal("10.00"))
        self.pizza_2 = Pizza.objects.create(
            nombre="Prosciutto", precio=Decimal("12.50")
        )

        # --- DATOS PARA IMPLEMENTAR (PRÁCTICA) ---
        # TODO: Una vez hayas creado los modelos Cliente y Pedido en models.py:
        # 1. Descomenta la importación arriba.
        # 2. Crea aquí una instancia de 'self.cliente' (ej: Cliente.objects.create(...))
        # 3. Crea aquí una instancia de 'self.pedido' asociada a ese cliente.
        # Esto te permitirá usar self.cliente y self.pedido en los tests de abajo.
        self.cliente = None
        self.pedido = None

    # --- TESTS DE REFERENCIA (YA IMPLEMENTADOS) ---
    # Los siguientes tests verifican el comportamiento básico de los modelos
    # que se han implementado en clase.

    def test_creacion_topping_ok(self):
        """Referencia: Verifica la creación correcta de un Topping."""
        self.assertEqual(Topping.objects.count(), 1)
        self.assertEqual(self.topping.nombre, "Extra Queso")
        self.assertTrue(self.topping.es_vegetariano)

    def test_representacion_str_topping(self):
        """Referencia: El __str__ de Topping debe devolver su nombre."""
        self.assertEqual(str(self.topping), "Extra Queso")

    def test_creacion_proveedor_ok(self):
        """Referencia: Verifica la creación correcta de un Proveedor."""
        self.assertEqual(Proveedor.objects.count(), 1)
        self.assertEqual(self.proveedor.nombre, "Proveedor Central")
        self.assertEqual(self.proveedor.email, "central@pizzas.com")

    def test_representacion_str_proveedor(self):
        """Referencia: El __str__ de Proveedor debe devolver su nombre."""
        self.assertEqual(str(self.proveedor), "Proveedor Central")

    def test_creacion_pizza_ok(self):
        """Referencia: Verifica la creación correcta de una Pizza."""
        self.assertEqual(Pizza.objects.count(), 2)
        self.assertEqual(self.pizza_1.nombre, "Margarita")
        self.assertEqual(self.pizza_1.precio, Decimal("10.00"))

    def test_representacion_str_pizza(self):
        """Referencia: El __str__ de Pizza debe devolver su nombre."""
        self.assertEqual(str(self.pizza_1), "Margarita")

    def test_pizza_con_toppings(self):
        """Referencia: Verifica la asignación de toppings a una pizza."""
        self.pizza_1.toppings.add(self.topping)
        self.assertIn(self.topping, self.pizza_1.toppings.all())

    # --- TESTS PARA IMPLEMENTAR POR EL ALUMNO ---
    # Completa los siguientes tests para evaluar tu implementación
    # de los modelos Cliente y Pedido.

    def test_creacion_cliente_ok(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que el objeto 'self.cliente' se ha creado correctamente
        y que sus atributos (nombre, email, telefono) coinciden con los
        proporcionados en el setUp.
        """
        pass

    def test_creacion_cliente_email_duplicado_falla(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que la base de datos impide crear un cliente con un email
        que ya existe. Debes usar un bloque `with self.assertRaises(IntegrityError):`
        para asegurar que se lanza la excepción correcta.
        """
        pass

    def test_representacion_str_cliente(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que el método __str__ del modelo Cliente devuelve
        correctamente el nombre del cliente.
        """
        pass

    def test_creacion_pedido_ok(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que el objeto 'self.pedido' se ha creado correctamente,
        que está asociado al cliente correcto y que su dirección de entrega
        es la esperada.
        """
        pass

    def test_pedido_asociado_a_pizzas(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que el pedido 'self.pedido' tiene asociadas las dos pizzas
        (self.pizza_1 y self.pizza_2) que se le añadieron en el setUp.
        """
        pass

    def test_representacion_str_pedido(self):
        """
        [TAREA - 0.25 PUNTOS]
        Verifica que el método __str__ del modelo Pedido devuelve una
        cadena que contiene el nombre del cliente y la dirección de entrega.
        """
        pass

    def test_metodo_calcular_total_pedido(self):
        """
        [TAREA - 0.5 PUNTOS]
        Verifica que el método 'calcular_total()' del modelo Pedido funciona
        correctamente. Debe sumar los precios de 'self.pizza_1' y 'self.pizza_2'.
        El total esperado es 22.50 (10.00 + 12.50).
        """
        pass
