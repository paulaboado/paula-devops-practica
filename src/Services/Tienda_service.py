"""Módulo de servicios para gestionar la tienda online."""

from typing import Dict, List, Optional
from models.Pedido import Pedido
from models.Producto import Producto
from models.Usuario import Administrador, Cliente, Usuario


class TiendaService:
    """Servicio encargado de gestionar productos, usuarios y pedidos."""

    def __init__(self) -> None:
        """Inicializa las listas de la tienda."""
        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []
        self.pedidos: List[Pedido] = []

    def registrar_usuario(
        self,
        nombre: str,
        email: str,
        tipo: str = "cliente",
        direccion: Optional[str] = None,
    ) -> Usuario:
        """Registra un nuevo cliente o administrador.

        Args:
            nombre (str): Nombre completo.
            email (str): Correo electrónico.
            tipo (str, optional): Tipo de usuario. Por defecto, cliente.
            direccion (Optional[str], optional): Dirección del cliente.
        
        Returns:
            Usuario: Usuario creado.
        """
        if tipo.lower() == "administrador":
            usuario = Administrador(nombre, email)
        else:
            if not direccion:
                direccion = "Sin dirección"
            usuario = Cliente(nombre, email, direccion)

        self.usuarios.append(usuario)
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        """Devuelve todos los usuarios registrados.

        Returns:
            List[Usuario]: Lista de usuarios.
        """
        return self.usuarios

    def obtener_usuario(self, usuario_id: str) -> Optional[Usuario]:
        """Busca un usuario mediante su identificador.

        Args:
            usuario_id (str): Identificador del usuario.

        Returns:
            Optional[Usuario]: Usuario encontrado o None si no existe.
        """
        return next((u for u in self.usuarios if u.id == usuario_id), None)

    def anadir_producto(self, producto: Producto) -> None:
        """Añade un producto al inventario.

        Args:
            producto (Producto): Producto que se quiere añadir.
        """
        self.productos.append(producto)

    def eliminar_producto(self, producto_id: str) -> bool:
        """Elimina un producto mediante su identificador.

        Args:
            producto_id (str): Identificador del producto.

        Returns:
            bool: True si se elimina y False si no se encuentra.
        """
        for prod in self.productos:
            if prod.id == producto_id:
                self.productos.remove(prod)
                return True
        return False

    def listar_productos(self) -> List[Producto]:
        """Devuelve todos los productos disponibles.

        Returns:
            List[Producto]: Lista de productos.
        """
        return self.productos

    def obtener_producto(self, producto_id: str) -> Optional[Producto]:
        """Busca un producto mediante su identificador.

        Args:
            producto_id (str): Identificador del producto.

        Returns:
            Optional[Producto]: Producto encontrado o None si no existe.
        """
        return next((p for p in self.productos if p.id == producto_id), None)

    def realizar_pedido(
        self, usuario_id: str, productos_solicitados: Dict[str, int]
    ) -> Optional[Pedido]:
        """Realiza un pedido comprobando usuario y stock.

        Args:
            usuario_id (str): ID del usuario que realiza el pedido.
            productos_solicitados (Dict[str, int]): Productos y cantidades.

        Returns:
            Optional[Pedido]: Pedido creado o None si hay algún error.
        """
        cliente = next(
            (u for u in self.usuarios if u.id == usuario_id and isinstance(u, Cliente)),
            None,
        )
        if not cliente:
            print(f"Error: Usuario con ID '{usuario_id}' no encontrado o no es un Cliente.")
            return None

        items_pedido: Dict[Producto, int] = {}
        for prod_id, cantidad in productos_solicitados.items():
            producto = next((p for p in self.productos if p.id == prod_id), None)
            if not producto:
                print(f"Error: Producto con ID '{prod_id}' no existe.")
                return None
            if not producto.hay_stock(cantidad):
                print(
                    f"Error: Stock insuficiente para '{producto.nombre}'. "
                    f"Requerido: {cantidad}, Disponible: {producto.stock}"
                )
                return None
            items_pedido[producto] = cantidad

        for producto, cantidad in items_pedido.items():
            producto.actualizar_stock(-cantidad)

        nuevo_pedido = Pedido(cliente, items_pedido)
        self.pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def listar_pedidos_usuario(self, usuario_id: str) -> List[Pedido]:
        """Devuelve los pedidos del usuario ordenados por fecha.

        Args:
            usuario_id (str): Identificador del cliente.

        Returns:
            List[Pedido]: Pedidos del usuario ordenados cronológicamente.
        """
        pedidos_cliente = [p for p in self.pedidos if p.cliente.id == usuario_id]
        pedidos_cliente.sort(key=lambda p: p.fecha)
        return pedidos_cliente