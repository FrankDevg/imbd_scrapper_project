# infrastructure/scraper/factory.py

from domain.scraper_interface import ScraperInterface
from infrastructure.scraper.imdb_scraper import ImdbScraper

def get_scraper(source: str) -> ScraperInterface:
    """
    Devuelve una implementación concreta de ScraperInterface según el nombre fuente.
    """
    source_clean = source.strip().lower()

    if source_clean == "imdb":
        return ImdbScraper()

   

    raise ValueError(f" Scraper no soportado: '{source}'")
