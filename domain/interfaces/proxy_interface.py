# domain/interfaces/proxy_interface.py

from abc import ABC, abstractmethod
from typing import Optional, Dict

class ProxyProviderInterface(ABC):
    @abstractmethod
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        Devuelve un proxy a utilizar (TOR, autenticado, desde lista o ninguno).
        """
        pass

    @abstractmethod
    def get_proxy_location(self, proxy: Optional[Dict[str, str]]) -> tuple[str, str, str]:
        """
        Consulta la IP pública, ciudad y país usando el proxy.
        """
        pass
