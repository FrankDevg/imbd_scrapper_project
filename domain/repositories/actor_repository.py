from abc import ABC, abstractmethod
from domain.models.actor import Actor

class ActorRepository(ABC):
    """
    Interfaz de repositorio para la entidad Actor.

    Define el contrato que deben cumplir las implementaciones encargadas
    de guardar actores, ya sea en CSV, base de datos u otro medio de persistencia.
    """

    @abstractmethod
    def save(self, actor: Actor) -> None:
        """
        Guarda un actor en el medio de persistencia correspondiente.

        Args:
            actor (Actor): Objeto Actor que se desea guardar.
        """
        pass
