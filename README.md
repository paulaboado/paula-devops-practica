# paula-devops-practica

**Autora:** Paula Boado Ferreira
**Asignatura:** Arquitectura del Software


## Descripción
API REST de una tienda online desarrollada con FastAPI en la Práctica 2.
Permite registrar usuarios (clientes y administradores), gestionar productos
(genéricos, electrónicos y ropa) y realizar pedidos con control de stock.
Los datos se guardan en memoria mientras la aplicación está en marcha.


## Estructura del proyecto
```
paula-devops-practica/
├── src/
│ ├── main.py │ ├── models/ │ └── Services/
│ └── Tienda
_
service.py ├── requirements.txt ├──
.gitignore
└── README.md
```
# API FastAPI: esquemas y endpoints
# Dominio: Usuario, Producto, Pedido
# Lógica de negocio de la tienda
# Dependencias con versiones fijadas
## Requisitos
- Python 3.12 o superior
- Dependencias de
`
requirements.txt` (FastAPI, Uvicorn y Pydantic)
## Cómo ejecutar
```
bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
Después abre http://127.0.0.1:8000/docs para probar la API desde el navegador.
## Endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/usuarios
` | Registra un cliente o un administrador |
| GET | `/usuarios
` | Lista los usuarios |
| GET | `/usuarios/{usuario
_
id}` | Obtiene un usuario |
| POST | `/productos
` | Crea un producto (generico, electronico o ropa) |
| GET | `/productos
` | Lista los productos |
| GET | `/productos/{producto
_
id}` | Obtiene un producto |
| DELETE | `/productos/{producto
_
id}` | Elimina un producto |
| POST | `/pedidos
` | Crea un pedido y descuenta el stock |
| GET | `/usuarios/{cliente
_
id}/pedidos
` | Pedidos de un cliente, por fecha |
