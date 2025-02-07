# RESTful APIs: Apolo Product Management

Este proyecto consiste en dos APIs RESTful desarrolladas con Django REST Framework. Las APIs interactúan entre sí para gestionar productos y órdenes.

---

## Estructura del Proyecto

1. **API 1: Product Manager**
   - Gestiona productos con endpoints para:
     - Listar productos.
     - Crear un nuevo producto.
     - Actualizar el stock de un producto.

2. **API 2: Order Manager**
   - Gestiona órdenes e interactúa con la API 1 para:
     - Validar la disponibilidad de productos.
     - Reducir el stock cuando se realiza un pedido.
     - Proporcionar detalles de las ordenes, incluyendo el precio total de cada una.

---

## Instalación y Configuración

### Pasos para Configurar el Proyecto

Todas las instrucciones a continuación deben ejecutarse en un terminal de Windows.

1. **Clona el repositorio**
   ```bat
   git clone https://github.com/djg-91/apolo-product-management
   cd apolo-product-management
   ```

2. **Crea un entorno virtual (opcional)**
   ```bat
   python -m venv ..\apolo-product-management_env
   ..\apolo-product-management_env\Scripts\activate
   ```

3. **Instala las dependencias**
   ```bat
   pip install -r requirements.txt
   ```

4. **Ejecuta las migraciones**
   ```bat
   python .\product_manager\manage.py makemigrations
   python .\product_manager\manage.py migrate
   python .\order_manager\manage.py makemigrations
   python .\order_manager\manage.py migrate
   ```

5. **Ejecuta las APIs**
   1. Para ejecutar ambas APIs al mismo tiempo (recomendado para garantizar la comunicación entre ellas):
      ```bat
      .\run.bat
      ```

   2. Para ejecutar solo la API Product Manager:
      ```bat
      python .\product_manager\manage.py runserver
      ```
   
   3. Para ejecutar solo la API Order Manager:
      ```bat
      python .\order_manager\manage.py runserver
      ```

---

## Endpoints: Swagger

Cada API cuenta con su propia documentación interactiva generada con Swagger. Puedes acceder a esta documentación a través de las siguientes URLs:

### **API 1: Product Manager**
- **URL:** `/api/docs` (e.g. `127.0.0.1:8000/api/docs`)

### **API 2: Order Manager**
- **URL:** `/api/docs` (e.g. `127.0.0.1:8001/api/docs`)

---

## Endpoints: Descripción y ejemplos

### **API 1: Product Manager**
#### 1. Obtener lista de productos
- **Método**: `GET`
- **URL**: `/api/products/`
- **Descripción**: Devuelve una lista de todos los productos.
- **Respuesta (200)**:
  ```json
  [
    {
      "id": 1,
      "name": "Producto A",
      "price": 10.99,
      "stock": 100
    },
    {
      "id": 2,
      "name": "Producto B",
      "price": 15.49,
      "stock": 50
    }
  ]
  ```

#### 2. Obtener detalles de un producto
- **Método**: `GET`
- **URL**: `/api/products/{id}/`
- **Descripción**: Devuelve los detalles de un producto específico.
- **Respuesta (200)**:
  ```json
  {
    "id": 1,
    "name": "Producto A",
    "price": 10.99,
    "stock": 100
  }
  ```

#### 3. Crear un nuevo producto
- **Método**: `POST`
- **URL**: `/api/products/`
- **Descripción**: Crea un nuevo producto con los datos proporcionados.
- **Cuerpo de la solicitud**:
  ```json
  {
    "name": "Producto C",
    "price": 12.99,
    "stock": 20
  }
  ```
- **Respuesta (201)**:
  ```json
  {
    "id": 3,
    "name": "Producto C",
    "price": 12.99,
    "stock": 20
  }
  ```

#### 4. Actualizar el stock de un producto
- **Método**: `PATCH`
- **URL**: `/api/products/{id}/stock/`
- **Descripción**: Actualiza el stock de un producto por su ID.
- **Cuerpo de la solicitud**:
  ```json
  {
    "stock": 15
  }
  ```
- **Respuesta (200)**:
  ```json
  {
    "id": 1,
    "name": "Producto A",
    "price": 10.99,
    "stock": 15
  }
  ```

### **API 2: Order Manager**
#### 1. Crear una nueva orden
- **Método**: `POST`
- **URL**: `/api/orders/`
- **Descripción**: Crea una nueva orden, validando la disponibilidad de stock y reduciéndolo en la API Product Manager.
- **Cuerpo de la solicitud**:
  ```json
  {
    "products": [
      {"id": 1, "quantity": 2},
      {"id": 2, "quantity": 1}
    ]
  }
  ```
- **Respuesta (201)**:
  ```json
  {
    "id": 1,
    "products": [
      {"id": 1, "name": "Producto A", "quantity": 2, "price": 10.99},
      {"id": 2, "name": "Producto B", "quantity": 1, "price": 15.49}
    ],
    "total_price": 37.47
  }
  ```


#### 2. Obtener lista de ordenes
- **Método**: `GET`
- **URL**: `/api/orders/`
- **Descripción**: Devuelve una lista de todas las ordenes.
- **Respuesta (200)**:
  ```json
  [
  {
    "id": 1,
    "created_at": "2025-02-04T09:49:24.294928Z",
    "products": [
      {"id": 1, "name": "Producto A", "quantity": 2, "price": 10.99},
      {"id": 2, "name": "Producto B", "quantity": 1, "price": 15.49}
    ],
    "total_price": 37.47
  },
  {
    "id": 2,
    "created_at": "2025-02-06T12:25:24.132927Z",
    "products": [
      {"id": 1, "name": "Producto A", "quantity": 2, "price": 10.99},
      {"id": 2, "name": "Producto B", "quantity": 1, "price": 15.49}
    ],
    "total_price": 37.47
  }
  ]
  ```
---
