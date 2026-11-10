"""Punto de entrada de la API REST de la tienda online.

main.py es la capa de exposición del servicio: define los esquemas Pydantic
(qué datos entran y salen) y los endpoints, que usan la lógica de TiendaService.

Ejecutar desde la carpeta Tienda_online con:  uvicorn main:app --reload
"""

from datetime import datetime
from typing import List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from models.Producto import Producto, ProductoElectronico, ProductoRopa
from models.Usuario import Cliente
from Services.Tienda_service import TiendaService

app = FastAPI(title="Tienda Online API")

# Una única tienda para toda la aplicación (los datos se guardan en memoria).
tienda = TiendaService()


@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse(url="/docs")


# =============================================================================
# PARTE 1: ESQUEMAS (Pydantic)
# =============================================================================

# ----- Usuario -----
class UsuarioCreate(BaseModel):
    nombre: str = Field(min_length=1)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    tipo: Literal["cliente", "administrador"]
    direccion_postal: Optional[str] = None


class UsuarioRead(BaseModel):
    id: str
    nombre: str
    email: str
    es_admin: bool


# ----- Producto -----
class ProductoCreate(BaseModel):
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str = Field(min_length=1)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)
    meses_garantia: Optional[int] = Field(default=None, ge=0)  # solo electrónicos
    talla: Optional[str] = None  # solo ropa
    color: Optional[str] = None  # solo ropa


class ProductoRead(BaseModel):
    id: str
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None


# ----- Pedido -----
class PedidoItemCreate(BaseModel):
    producto_id: str
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    cliente_id: str
    items: List[PedidoItemCreate] = Field(min_length=1)


class PedidoItemRead(BaseModel):
    producto_id: str
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: str
    fecha: datetime
    cliente_id: str
    total: float
    items: List[PedidoItemRead]


# ----- Funciones auxiliares: pasan de objeto de dominio a esquema de salida -----
def usuario_a_read(usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.is_admin(),
    )


def producto_a_read(producto: Producto) -> ProductoRead:
    if isinstance(producto, ProductoElectronico):
        return ProductoRead(
            id=producto.id, tipo="electronico", nombre=producto.nombre,
            precio=producto.precio, stock=producto.stock,
            meses_garantia=producto.garantia_meses,
        )
    if isinstance(producto, ProductoRopa):
        return ProductoRead(
            id=producto.id, tipo="ropa", nombre=producto.nombre,
            precio=producto.precio, stock=producto.stock,
            talla=producto.talla, color=producto.color,
        )
    return ProductoRead(
        id=producto.id, tipo="generico", nombre=producto.nombre,
        precio=producto.precio, stock=producto.stock,
    )


def pedido_a_read(pedido) -> PedidoRead:
    items = []
    for producto, cantidad in pedido.productos_cantidad.items():
        items.append(PedidoItemRead(
            producto_id=producto.id,
            nombre=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=cantidad,
            subtotal=producto.precio * cantidad,
        ))
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente.id,
        total=pedido.total,
        items=items,
    )


# =============================================================================
# PARTE 2: ENDPOINTS
# =============================================================================

# ----- Usuarios -----
@app.post("/usuarios", response_model=UsuarioRead, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    if usuario.tipo == "cliente" and not usuario.direccion_postal:
        raise HTTPException(status_code=400, detail="Un cliente necesita dirección postal")
    if any(u.email == usuario.email for u in tienda.listar_usuarios()):
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese email")

    nuevo = tienda.registrar_usuario(
        usuario.nombre, usuario.email, usuario.tipo, usuario.direccion_postal
    )
    return usuario_a_read(nuevo)


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(usuario_id: str):
    usuario = tienda.obtener_usuario(usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_a_read(usuario)


@app.get("/usuarios", response_model=List[UsuarioRead])
def listar_usuarios():
    return [usuario_a_read(u) for u in tienda.listar_usuarios()]


# ----- Productos -----
@app.post("/productos", response_model=ProductoRead, status_code=201,
          response_model_exclude_none=True)
def crear_producto(producto: ProductoCreate):
    if producto.tipo == "electronico":
        if producto.meses_garantia is None:
            raise HTTPException(status_code=400, detail="Un electrónico necesita meses_garantia")
        nuevo = ProductoElectronico(
            producto.nombre, producto.precio, producto.stock, producto.meses_garantia
        )
    elif producto.tipo == "ropa":
        if not producto.talla or not producto.color:
            raise HTTPException(status_code=400, detail="La ropa necesita talla y color")
        nuevo = ProductoRopa(
            producto.nombre, producto.precio, producto.stock, producto.talla, producto.color
        )
    else:
        nuevo = Producto(producto.nombre, producto.precio, producto.stock)

    tienda.anadir_producto(nuevo)
    return producto_a_read(nuevo)


@app.get("/productos", response_model=List[ProductoRead], response_model_exclude_none=True)
def listar_productos():
    return [producto_a_read(p) for p in tienda.listar_productos()]


@app.get("/productos/{producto_id}", response_model=ProductoRead,
         response_model_exclude_none=True)
def obtener_producto(producto_id: str):
    producto = tienda.obtener_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_a_read(producto)


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str):
    if not tienda.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado correctamente"}


# ----- Pedidos -----
@app.post("/pedidos", response_model=PedidoRead, status_code=201)
def crear_pedido(pedido: PedidoCreate):
    # 1. El cliente debe existir y ser un Cliente (no un administrador)
    cliente = tienda.obtener_usuario(pedido.cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    if not isinstance(cliente, Cliente):
        raise HTTPException(status_code=400, detail="Solo los clientes pueden hacer pedidos")

    # 2. Juntamos las líneas en un diccionario {producto_id: cantidad},
    #    que es lo que espera TiendaService.realizar_pedido
    productos_solicitados = {}
    for item in pedido.items:
        productos_solicitados[item.producto_id] = (
            productos_solicitados.get(item.producto_id, 0) + item.cantidad
        )

    # 3. Cada producto debe existir y tener stock suficiente
    for producto_id, cantidad in productos_solicitados.items():
        producto = tienda.obtener_producto(producto_id)
        if producto is None:
            raise HTTPException(status_code=404, detail=f"Producto {producto_id} no encontrado")
        if not producto.hay_stock(cantidad):
            raise HTTPException(
                status_code=400, detail=f"Stock insuficiente para '{producto.nombre}'"
            )

    # 4. Todo correcto: TiendaService crea el pedido y descuenta el stock
    nuevo = tienda.realizar_pedido(pedido.cliente_id, productos_solicitados)
    return pedido_a_read(nuevo)


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead])
def pedidos_de_cliente(cliente_id: str):
    if tienda.obtener_usuario(cliente_id) is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return [pedido_a_read(p) for p in tienda.listar_pedidos_usuario(cliente_id)]


# Permite arrancar la API también con el botón "Run" o con: python3 main.py
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
