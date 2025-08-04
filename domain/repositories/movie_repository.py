from abc import ABC, abstractmethod
from domain.models.movie import Movie

class MovieRepository(ABC):
    """
    Interfaz de repositorio para la entidad Movie.

    Define el contrato que deben cumplir las implementaciones encargadas
    de guardar películas, ya sea en archivos CSV, bases de datos relacionales
    o cualquier otro sistema de persistencia.
    """

    @abstractmethod
    def save(self, movie: Movie) -> None:
        """
        Guarda una película en el medio de persistencia correspondiente.

        Args:
            movie (Movie): Objeto Movie que contiene la información a guardar.
        """
        pass
