"""Módulo que define las clases de productos para la tienda online."""

from uuid import uuid4


class Producto:
    """Clase base que representa un producto general en la tienda."""

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        """Inicializa una nueva instancia de Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio unitario del producto.
            stock (int): Cantidad de unidades disponibles.
        """
        self.id: str = str(uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, unidades: int) -> bool:
        """Comprueba si existe suficiente stock.

        Args:
            unidades (int): Número de unidades solicitadas.

        Returns:
            bool: True si hay stock suficiente, False en caso contrario.
        """
        return self.stock >= unidades

    def actualizar_stock(self, unidades: int) -> None:
        """Modifica la cantidad de stock disponible.

        Args:
            unidades (int): Número de unidades que se añaden o eliminan.
        """
        self.stock += unidades

    def __str__(self) -> str:
        """Devuelve la información básica del producto.

        Returns:
            str: Información del producto.
        """
        return f"[{self.id[:8]}] {self.nombre} - Precio: {self.precio:.2f}€ - Stock: {self.stock}"


class ProductoElectronico(Producto):
    """Clase que representa un producto electrónico con garantía."""

    def __init__(
        self, nombre: str, precio: float, stock: int, garantia_meses: int
    ) -> None:
        """Inicializa un producto electrónico.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.
            stock (int): Unidades disponibles.
            garantia_meses (int): Duración de la garantía.
        """
        super().__init__(nombre, precio, stock)
        self.garantia_meses: int = garantia_meses

    def __str__(self) -> str:
        """Devuelve la información del producto electrónico.

        Returns:
            str: Información del producto y su garantía.
        """
        return f"{super().__str__()} - Garantía: {self.garantia_meses} meses"


class ProductoRopa(Producto):
    """Clase que representa un artículo de ropa."""

    def __init__(
        self, nombre: str, precio: float, stock: int, talla: str, color: str
    ) -> None:
        """Inicializa un producto de ropa.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.
            stock (int): Unidades disponibles.
            talla (str): Talla de la prenda.
            color (str): Color de la prenda.
        """
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        """Devuelve la información del producto de ropa.

        Returns:
            str: Información del producto, talla y color.
        """
        return f"{super().__str__()} - Talla: {self.talla} - Color: {self.color}"