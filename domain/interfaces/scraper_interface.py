from abc import ABC, abstractmethod
from typing import List
from domain.models.movie import Movie

class ScraperInterface(ABC):
    @abstractmethod
    def scrape(self) -> List[Movie]:
        pass
