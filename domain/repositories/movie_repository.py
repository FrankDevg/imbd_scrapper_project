from abc import ABC, abstractmethod
from typing import Optional
from domain.models.movie import Movie

class MovieRepository(ABC):
    """
    Interfaz de repositorio para la entidad Movie.

    Define el contrato que deben cumplir las implementaciones encargadas
    de guardar y buscar películas.
    """

    @abstractmethod
    def save(self, movie: Movie) -> Movie:
        """
        Guarda una película y retorna la entidad guardada (potencialmente con el ID asignado).

        Args:
            movie (Movie): Objeto Movie que contiene la información a guardar.
        
        Returns:
            Movie: La entidad Movie tal como fue guardada, incluyendo cualquier
                   campo generado por la base de datos (ej. id).
        """
        pass

    @abstractmethod
    def find_by_imdb_id(self, imdb_id: str) -> Optional[Movie]:
        """
        Busca una película por su ID de IMDb para evitar duplicados.

        Args:
            imdb_id (str): El ID único de IMDb (ej. 'tt0111161').

        Returns:
            Optional[Movie]: El objeto Movie si se encuentra, de lo contrario None.
        """
        pass