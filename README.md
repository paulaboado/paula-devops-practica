# paula-devops-practica
**Autora:** Paula Boado Ferreira
**Asignatura:** Arquitectura del Software

## Descripción
API REST de una tienda online desarrollada con FastAPI en la Práctica 2.
Permite registrar usuarios (clientes y administradores), gestionar productos
(genéricos, electrónicos y ropa) y realizar pedidos con control de stock.
Los datos se guardan en memoria mientras la aplicación está en marcha.

En la Práctica 3.2 la API se ha contenerizado con Docker y la imagen está
publicada en Docker Hub.

## Estructura del proyecto
```
paula-devops-practica/
├── src/
│   ├── main.py                 # API FastAPI: endpoints
│   ├── models/                 # Usuario, Producto, Pedido
│   └── Services/
│       └── Tienda_service.py   # Lógica de negocio de la tienda
├── Dockerfile                  # Receta de la imagen Docker
├── .dockerignore               # Lo que no entra en la imagen
├── requirements.txt            # Dependencias con versiones fijadas
├── .gitignore
└── README.md
```

## Requisitos
- Python 3.12 o superior (para ejecutar sin Docker)
- Docker Desktop (para ejecutar con Docker)

## Cómo ejecutar sin Docker
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src && uvicorn main:app --reload
```
Después abre http://127.0.0.1:8000/docs

## Docker

### Imagen publicada
https://hub.docker.com/r/paulabetanzos2006/paula-devops-practica
Etiquetas: `1.0.0` y `latest` (para `linux/amd64` y `linux/arm64`).

### 1. Construir la imagen
```bash
docker build -t paula-devops-practica:1.0.0 .
docker images paula-devops-practica
```

### 2. Ejecutar el contenedor
```bash
docker run -d --name paula-api -p 8000:8000 paula-devops-practica:1.0.0
docker logs paula-api
```
- `-d` lo deja en segundo plano.
- `--name paula-api` le da un nombre.
- `-p 8000:8000` conecta el puerto 8000 del ordenador con el del contenedor.

Usar otro puerto con la variable PORT:
```bash
docker run -d --name paula-9000 -e PORT=9000 -p 9000:9000 paula-devops-practica:1.0.0
```

Parar y borrar:
```bash
docker rm -f paula-api paula-9000
```

### 3. Descargar la imagen de Docker Hub (pull)
```bash
docker pull paulabetanzos2006/paula-devops-practica:1.0.0
docker run -d --name paula-hub -p 8000:8000 paulabetanzos2006/paula-devops-practica:1.0.0
```

### 4. Publicar una nueva versión (push)
```bash
docker login
docker buildx build --platform linux/amd64,linux/arm64 -t paulabetanzos2006/paula-devops-practica:1.0.0 -t paulabetanzos2006/paula-devops-practica:latest --push .
```

### Variables de entorno
| Variable | Valor por defecto | Para qué sirve |
|----------|-------------------|----------------|
| `PORT` | `8000` | Puerto en el que escucha Uvicorn dentro del contenedor |

La aplicación no usa contraseñas ni claves, así que no hay secretos que configurar.

### Pruebas
1. Abre http://localhost:8000/docs y verás Swagger con Usuarios, Productos y Pedidos.
2. Crea un usuario y un producto (POST), y después un pedido de 2 unidades: el total sale 11.0 y el stock baja de 10 a 8.
3. El contenedor no se ejecuta como root: `docker exec paula-api whoami` devuelve `appuser`.

## Flujo de trabajo con Git
- `main`: rama estable y protegida. Solo recibe cambios mediante Pull Request.
- `feature/`: una rama por tarea (`feature/docs`, `feature/docker`).
- Commits pequeños con prefijo: `feat:`, `docs:`, `chore:`, `fix:`.
