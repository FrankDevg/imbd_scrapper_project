
from abc import ABC, abstractmethod
from typing import Optional, Dict

class ProxyProviderInterface(ABC):
    """
    Interfaz para proveedores de proxies.

    Esta interfaz define los métodos que cualquier implementación de proveedor de proxy debe cumplir,
    ya sea TOR, proxy autenticado, proxy desde lista, etc.
    """

    @abstractmethod
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retorna un diccionario con los parámetros del proxy actual a utilizar (por ejemplo:
        {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}).

        Returns:
            Optional[Dict[str, str]]: Proxy a utilizar, o None si no se usa proxy.
        """
        pass

    @abstractmethod
    def get_proxy_location(self, proxy: Optional[Dict[str, str]]) -> tuple[str, str, str]:
        """
        Obtiene la información geográfica asociada al proxy (IP pública, ciudad, país).

        Args:
            proxy (Optional[Dict[str, str]]): Diccionario con configuración del proxy.

        Returns:
            tuple[str, str, str]: Una tupla con (IP pública, ciudad, país).
        """
        pass
