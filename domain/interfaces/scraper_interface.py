from abc import ABC, abstractmethod
from typing import List
from domain.models.movie import Movie

class ScraperInterface(ABC):
    """
    Interfaz base para scrapers de películas.

    Cualquier clase que implemente esta interfaz debe proporcionar una implementación
    del método `scrape`, que retorna una lista de objetos Movie extraídos de alguna fuente.
    """

    @abstractmethod
    def scrape(self) -> List[Movie]:
        """
        Ejecuta el proceso de scraping y devuelve una lista de películas extraídas.

        Returns:
            List[Movie]: Lista de objetos Movie con los datos obtenidos del scraping.
        """
        pass
