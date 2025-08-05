from abc import ABC, abstractmethod
from typing import List
from domain.models.movie_actor import MovieActor

class MovieActorRepository(ABC):
    """
    Interfaz de repositorio para manejar la relación N:M entre películas y actores.
    """

    @abstractmethod
    def save(self, relation: MovieActor) -> None:
        """
        Guarda una única relación película-actor.

        Útil para casos donde solo se necesita añadir una asociación puntual.

        Args:
            relation (MovieActor): La relación a persistir.
        """
        pass

    @abstractmethod
    def save_many(self, relations: List[MovieActor]) -> None:
        """
        Guarda una lista de relaciones película-actor de forma eficiente.

        Ideal para cuando se procesa una película con múltiples actores a la vez,
        ya que permite optimizar la operación de escritura.

        Args:
            relations (List[MovieActor]): Lista de relaciones MovieActor a persistir.
        """
        pass