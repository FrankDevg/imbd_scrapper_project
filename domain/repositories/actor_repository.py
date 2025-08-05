from abc import ABC, abstractmethod
from typing import Optional
from domain.models.actor import Actor

class ActorRepository(ABC):
    """
    Interfaz de repositorio para la entidad Actor.
    """

    @abstractmethod
    def save(self, actor: Actor) -> Actor:
        """
        Guarda un actor y retorna la entidad guardada.
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Actor]:
        """
        Busca un actor por su nombre.

        Args:
            name (str): Nombre del actor a buscar.

        Returns:
            Optional[Actor]: El objeto Actor si se encuentra, de lo contrario None.
        """
        pass