# infrastructure/scraper/factory.py

from domain.interfaces.scraper_interface import ScraperInterface
from infrastructure.scraper.imdb_scraper import ImdbScraper

def get_scraper(source: str) -> ScraperInterface:
    """
    Fábrica que retorna una implementación concreta de ScraperInterface según la fuente indicada.

    Esta función permite seleccionar dinámicamente el scraper apropiado a partir del nombre de la fuente.

    Args:
        source (str): Nombre de la fuente desde donde se desea hacer scraping (ej. "imdb").

    Returns:
        ScraperInterface: Instancia concreta del scraper correspondiente.

    Raises:
        ValueError: Si la fuente especificada no está soportada.
    """
    source_clean = source.strip().lower()

    if source_clean == "imdb":
        return ImdbScraper()

    raise ValueError(f"Scraper no soportado: '{source}'")
