from abc import ABC, abstractmethod
from typing import List
from domain.models.movie_actor import MovieActor

class MovieActorRepository(ABC):
    @abstractmethod
    def save(self, relations: List[MovieActor]) -> None:
        pass
