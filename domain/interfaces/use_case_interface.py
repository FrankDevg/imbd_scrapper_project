from abc import ABC, abstractmethod
from typing import Any

class UseCaseInterface(ABC):
    """
    Interfaz base para todos los casos de uso de la aplicación.

    Esta clase abstracta define el contrato que deben implementar todos los
    casos de uso concretos. Garantiza una estructura uniforme y permite 
    desacoplar la lógica de aplicación del resto del sistema.
    """

    @abstractmethod
    def execute(self, data: Any) -> None:
        """
        Ejecuta la lógica principal del caso de uso.

        Args:
            data (Any): Datos necesarios para ejecutar el caso de uso. 
                        Puede ser un objeto, diccionario u otro tipo dependiendo del contexto.

        Returns:
            None
        """
        pass
