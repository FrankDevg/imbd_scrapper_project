from abc import ABC, abstractmethod

class TorInterface(ABC):
    """
    Interfaz para el control de la red TOR.

    Define los métodos necesarios para rotar la IP y consultar la IP actual de salida a través de TOR.
    Las implementaciones pueden utilizar herramientas como el puerto de control de TOR o servicios externos.
    """

    @abstractmethod
    def rotate_ip(self) -> str:
        """
        Rota la dirección IP actual de la red TOR y retorna la nueva IP pública.

        Returns:
            str: Nueva IP pública obtenida tras la rotación.
        """
        pass

    @abstractmethod
    def get_current_ip(self) -> str:
        """
        Obtiene la IP pública actual de salida por la red TOR, sin realizar rotación.

        Returns:
            str: IP pública actual de TOR.
        """
        pass
