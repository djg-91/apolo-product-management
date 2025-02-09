# RESTful APIs: Apolo Product Management

Este proyecto consiste en dos APIs RESTful desarrolladas con Django REST Framework para gestionar productos y órdenes. Las APIs interactúan entre sí para proporcionar una solución completa de gestión de inventario y pedidos.

## Características principales

- **API 1: Product Manager**
  - Gestión completa de productos (CRUD)
  - Actualización de stock

- **API 2: Order Manager**
  - Creación y gestión de órdenes
  - Validación de disponibilidad de productos
  - Actualización automática de stock al realizar pedidos

## Estructura del Proyecto

### API 1: Product Manager

Endpoints:
- Crear un nuevo producto
- Listar productos disponibles
- Obtener información detallada de un producto
- Eliminar un producto
- Actualizar el stock de un producto

### API 2: Order Manager

Endpoints:
- Crear una nueva orden
- Listar órdenes disponibles (incluye precio total y detalle de productos)
- Obtener información detallada de una orden
- Eliminar una orden

## Instalación y Configuración

### Opción 1: Usando Docker (Recomendado)

#### Requisitos previos
- Docker
- Docker Compose

#### Pasos
1. Clonar el repositorio:
   ```bat
   git clone https://github.com/djg-91/apolo-product-management
   cd apolo-product-management
   ```

2. Construir y ejecutar los contenedores
   ```bash
   docker-compose up --build
   ```

### Opción 2: Ejecución manual

#### Requisitos previos
- Python 3.13
- Terminal de Windows

#### Pasos
1. Clonar el repositorio:
   ```bat
   git clone https://github.com/djg-91/apolo-product-management
   cd apolo-product-management
   ```

2. Crear y activar un entorno virtual (opcional pero recomendado):
   ```bat
   python -m venv ..\apolo-product-management_env
   ..\apolo-product-management_env\Scripts\activate
   ```

3. Instalar dependencias:
   ```bat
   pip install -r requirements.txt
   ```

4. Ejecutar migraciones:
   ```bat
   python .\product_manager\manage.py makemigrations
   python .\product_manager\manage.py migrate
   python .\order_manager\manage.py makemigrations
   python .\order_manager\manage.py migrate
   ```

5. Ejecutar las APIs:
- Ambas APIs simultáneamente (recomendado):
  ```
  .\run.bat
  ```
- Solo Product Manager:
  ```
  python .\product_manager\manage.py runserver
  ```
- Solo Order Manager:
  ```
  python .\order_manager\manage.py runserver
  ```

## Documentación de la API

Cada API cuenta con documentación interactiva generada con Swagger:

- **API 1: Product Manager**: `http://127.0.0.1:8000/api/docs`
- **API 2: Order Manager**: `http://127.0.0.1:8001/api/docs`

## Ejemplos de uso

### API 1: Product Manager

#### Crear un nuevo producto


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
#### 1. Crear un nuevo producto
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
  
#### 2. Obtener lista de productos
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

#### 3. Obtener detalles de un producto
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

#### 4. Eliminar un producto
- **Método**: `DELETE`
- **URL**: `/api/products/{id}/`
- **Descripción**: Elimina un producto específico por su ID.
- **Respuesta (204)**: Sin contenido.

#### 5. Actualizar el stock de un producto
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

#### 3. Obtener detalles de una orden
- **Método**: `GET`
- **URL**: `/api/orders/{id}/`
- **Descripción**: Devuelve los detalles de una orden específica por su ID.
- **Respuesta (200)**:
  ```json
  {
    "id": 1,
    "created_at": "2025-02-04T09:49:24.294928Z",
    "products": [
      {"id": 1, "name": "Producto A", "quantity": 2, "price": 10.99},
      {"id": 2, "name": "Producto B", "quantity": 1, "price": 15.49}
    ],
    "total_price": 37.47
  }
  ```

#### 4. Eliminar una orden
- **Método**: `DELETE`
- **URL**: `/api/orders/{id}/`
- **Descripción**: Elimina una orden específica por su ID.
- **Respuesta (204)**: Sin contenido.
