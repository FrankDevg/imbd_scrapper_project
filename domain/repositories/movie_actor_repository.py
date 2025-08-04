from abc import ABC, abstractmethod
from typing import List
from domain.models.movie_actor import MovieActor

class MovieActorRepository(ABC):
    """
    Interfaz de repositorio para manejar la relación N:M entre películas y actores.

    Esta interfaz define el contrato para guardar asociaciones entre películas y actores
    en un sistema de persistencia (CSV, base de datos, etc.).
    """

    @abstractmethod
    def save(self, relations: List[MovieActor]) -> None:
        """
        Guarda una lista de relaciones entre películas y actores.

        Args:
            relations (List[MovieActor]): Lista de relaciones MovieActor a persistir.
        """
        pass
