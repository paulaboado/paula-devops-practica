"""Módulo que define los tipos de usuarios de la tienda online."""

from uuid import uuid4


class Usuario:
    """Clase base que representa un usuario del sistema."""

    def __init__(self, nombre: str, email: str) -> None:
        """Crea una nueva instancia de Usuario.

        Args:
            nombre (str): Nombre completo del usuario.
            email (str): Dirección de correo electrónico.
        """
        self.id: str = str(uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """Comprueba si el usuario es administrador.

        Returns:
            bool: False para un usuario normal.
        """
        return False

    def __str__(self) -> str:
        """Muestra la información básica del usuario.

        Returns:
            str: Datos principales del usuario.
        """
        return f"[{self.id[:8]}] {self.nombre} ({self.email})"


class Cliente(Usuario):
    """Clase que representa a un cliente de la tienda."""

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        """Crea un nuevo cliente con su dirección.

        Args:
            nombre (str): Nombre completo.
            email (str): Correo electrónico.
            direccion (str): Dirección de entrega.
        """
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        """Muestra la información del cliente.

        Returns:
            str: Datos del cliente y su dirección.
        """
        return f"{super().__str__()} - Dirección: {self.direccion}"


class Administrador(Usuario):
    """Clase que representa a un administrador de la tienda."""

    def is_admin(self) -> bool:
        """Comprueba si el usuario tiene permisos de administrador.

        Returns:
            bool: True para un administrador.
        """
        return True

    def __str__(self) -> str:
        """Muestra la información del administrador.

        Returns:
            str: Datos del administrador.
        """
        return f"{super().__str__()} [ADMINISTRADOR]"