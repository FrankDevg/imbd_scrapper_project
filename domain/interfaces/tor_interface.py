from abc import ABC, abstractmethod

class TorInterface(ABC):
    @abstractmethod
    def rotate_ip(self) -> str:
        """Rota la IP TOR y devuelve la nueva IP"""
        pass

    @abstractmethod
    def get_current_ip(self) -> str:
        """Obtiene la IP TOR actual sin rotar"""
        pass
