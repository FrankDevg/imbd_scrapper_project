from abc import ABC, abstractmethod
from domain.models.movie import Movie

class MovieRepository(ABC):
    @abstractmethod
    def save(self, movie: Movie) -> None:
        pass
