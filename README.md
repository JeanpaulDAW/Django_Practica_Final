# Proyecto Django - Persistencia

## Descripción

Este proyecto está diseñado para **fines educativos**. Su objetivo es servir como base para la **Práctica Final** del módulo de persistencia de datos con Django. La estructura del proyecto sigue las mejores prácticas, incorporando `Docker`, `MySQL` y `Ruff` para garantizar un entorno de desarrollo profesional.

---

## 1. Instrucciones de Entrega

Este repositorio es una **plantilla**. Para realizar la práctica, sigue estos pasos obligatorios:

1.  **Crear tu repositorio:**
    -   Haz clic en el botón **"Use this template"** -> **"Create a new repository"**.
    -   Asigna un nombre a tu repositorio.
    -   **IMPORTANTE:** Marca el repositorio como **Privado**.
    -   Asegúrate de marcar la casilla **"Include all branches"**.
2.  **Clonar:** Clona tu nuevo repositorio privado en tu máquina local.
3.  **Entrega:** La entrega se realizará enviando el enlace de tu repositorio de GitHub a través del **Aula Virtual**.

---

## 2. Introducción y Objetivo de la Práctica

En esta práctica final, te enfrentarás a un reto de **Desarrollo Guiado por Tests (TDD)**. 

Te proporcionamos una suite de tests automatizados en `app/tests/` que actúan como una **especificación funcional** para una nueva funcionalidad de "Gestión de Pedidos".

**Tu objetivo es escribir el código de la aplicación (modelos, vistas y URLs) necesario para que todos los tests de la suite pasen con éxito.**

---

## 3. Sistema de Puntuación (Sobre 10)

La nota se calculará automáticamente basándose en los tests que pasen y la calidad del código:

-   **Tests de Modelos (2 puntos):** Puntuación total obtenida de los tests en `app/tests/test_models.py`.
-   **Tests de Vistas - API (6 puntos):** Puntuación total obtenida de los tests en `app/tests/test_views.py`.
-   **Calidad de Código - Linter (1 punto):** El comando `make lint` debe ejecutarse sin reportar ningún error.
-   **Calidad de Código - Revisión (1 punto):** Revisión manual de legibilidad, estructura y eficiencia.

---

## 4. Requisitos Previos y Configuración

### A. Requisitos
Asegúrate de tener instalados:
-   **Docker Desktop** (para ejecutar la base de datos y el servidor).
-   **Python 3.x** (para ejecutar herramientas locales).

### B. Configuración del Entorno Local
Para ejecutar el linter y tener autocompletado, crea un entorno virtual:

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**En Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
*(Si usas PowerShell y falla la activación, ejecuta: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*

### C. Arrancar la Aplicación
Con Docker Desktop abierto, ejecuta:

-   **macOS/Linux:** `make up`
-   **Windows:** `.\make.bat up`

Accede a [http://localhost:8000/admin](http://localhost:8000/admin) (Credenciales: `admin` / `admin`).

---

## 5. Instrucciones Paso a Paso de la Práctica

### Paso 1: Configurar tu Identificador Único (¡OBLIGATORIO!)
Los tests necesitan una "semilla" única para generar datos.
1.  Abre el fichero `app/tests/test_views.py`.
2.  Localiza la variable `GITHUB_USERNAME` al principio del fichero.
3.  **Cámbialo por tu usuario de GitHub**:
    ```python
    GITHUB_USERNAME = "tu_usuario_aqui" 
    ```
    *Si no realizas este paso, los tests fallarán automáticamente.*

### Paso 2: Implementar Modelos

Debes editar `app/models.py` para satisfacer los requisitos de los tests en `app/tests/test_models.py`.

**Procedimiento:**
1.  Abre el fichero `app/tests/test_models.py`.
2.  **Estudia los tests de referencia** para `Topping`, `Proveedor` y `Pizza`. Te muestran cómo se espera que funcionen los modelos básicos.
3.  Busca los tests marcados con `[TAREA - X PUNTOS]`. Estos son los tests que debes hacer pasar.
4.  Lee el docstring de cada test. Te explica **qué comportamiento se está evaluando** (ej. "Verifica que el email de Cliente sea único").
5.  Implementa la lógica en `app/models.py`.

#### Requisitos del Modelo `Cliente`
-   **`nombre`**: Campo de texto (`CharField`).
-   **`email`**: Campo de email (`EmailField`) que debe ser **único**.
-   **`telefono`**: Campo de texto (`CharField`), opcional.
-   **`fecha_alta`**: Campo de fecha (`DateField`), auto-completado al crear.
-   **`__str__`**: Debe devolver el nombre del cliente.

#### Requisitos del Modelo `Pedido`
-   **`cliente`**: Relación (`ForeignKey`) con `Cliente`.
-   **`pizzas`**: Relación muchos a muchos (`ManyToManyField`) con `Pizza`.
-   **`direccion_entrega`**: Campo de texto (`CharField`).
-   **`fecha_pedido`**: Fecha y hora (`DateTimeField`), auto-completado.
-   **`estado`**: Campo de texto (`CharField`), valor por defecto (ej. "Pendiente").
-   **`__str__`**: Cadena descriptiva (ej: `f"Pedido de {self.cliente}..."`).
-   **`calcular_total()`**: Método que devuelve la suma de los precios de las pizzas (tipo `Decimal`).

> **Nota:** Recuerda crear y aplicar las migraciones cada vez que modifiques los modelos:
> - `docker-compose run --rm servidor python manage.py makemigrations`
> - `docker-compose run --rm servidor python manage.py migrate`

### Paso 3: Implementar Vistas y URLs

Debes editar `app/views.py` y `app/urls.py` para satisfacer los tests en `app/tests/test_views.py`.

**Procedimiento:**
1.  Abre el fichero `app/tests/test_views.py`.
2.  **Estudia los tests de referencia** para las vistas de `Topping` y `Pizza`. Te muestran cómo deben funcionar los endpoints (códigos de estado, formato JSON, manejo de errores).
3.  Busca los tests marcados con `[TAREA - X PUNTOS]` para las vistas de `Cliente` y `Pedido`.
4.  Lee el docstring de cada test para entender **qué funcionalidad debe tener cada endpoint** (ej. "POST a /clientes/ debe crear un cliente" o "GET a /pedidos/ debe devolver una lista con el total calculado").
5.  Implementa los endpoints para listar y crear Clientes y Pedidos. Presta atención a:
    -   Los códigos de estado HTTP (`200 OK`, `201 Created`, `400 Bad Request`).
    -   El formato JSON de respuesta esperado por los tests.

---

## 6. Documentación y Pruebas Manuales (Opcional)

### A. Documentación de la API (Swagger/OpenAPI)
Hemos incluido un archivo `openapi.yml` en la raíz del proyecto. Este archivo contiene la **especificación completa de la API**, incluyendo tanto los endpoints que ya existen como los que debes implementar.

Puedes visualizarlo usando cualquier editor compatible con Swagger o pegando su contenido en [editor.swagger.io](https://editor.swagger.io/). Úsalo para entender qué estructura JSON exacta esperan recibir y devolver tus endpoints.

### B. Pruebas con Postman
Si deseas probar tu API manualmente además de usar los tests automáticos, puedes usar la colección de Postman incluida en el repositorio: `django-persistencia.postman_collection.json`.

1.  Importa el archivo JSON en tu aplicación Postman.
2.  Verás una colección llamada "django-persistencia" con ejemplos para `/pizzas` y `/toppings`.
3.  **¡Reto!** Crea tus propias peticiones (Request) dentro de esa colección para probar tus nuevos endpoints:
    -   `GET /clientes/` y `POST /clientes/`
    -   `GET /pedidos/` y `POST /pedidos/`
    
    Usa las peticiones existentes como plantilla y consulta el `openapi.yml` para configurar los Headers (`Content-Type: application/json`) y el Body de tus pruebas.

---

## 7. Verificación y Comandos Útiles

Usa el archivo `Makefile` (macOS/Linux) o `make.bat` (Windows) para ejecutar tareas comunes.

### Ejecutar Tests (Tu objetivo es que todos pasen)
-   **macOS/Linux:** `make test`
-   **Windows:** `.\make.bat test`

### Verificar Calidad de Código (Linter)
-   **macOS/Linux:** `make lint`
-   **Windows:** `.\make.bat lint`

### Otros Comandos
-   `make build`: Reconstruir imágenes Docker.
-   `make down`: Detener y borrar contenedores.
-   `make logs`: Ver logs en tiempo real.
-   `make shell`: Entrar a la terminal del contenedor.
