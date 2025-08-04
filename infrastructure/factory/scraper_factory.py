from domain.interfaces.use_case_interface import UseCaseInterface
from domain.interfaces.scraper_interface import ScraperInterface

def get_scraper(source: str = "imdb", engine: str = "requests", use_case: UseCaseInterface = None) -> ScraperInterface:
    """
    Devuelve una instancia del scraper según la fuente y el motor especificado.

    Args:
        source (str): Fuente del scraper, por defecto 'imdb'.
        engine (str): Motor de scraping (requests, tor, vpn, playwright, etc.).
        use_case (UseCaseInterface): Caso de uso que maneja la persistencia.

    Returns:
        ScraperInterface: Implementación concreta del scraper.
    """
    if use_case is None:
        raise ValueError("Se requiere un 'use_case' para inicializar el scraper.")

    source_clean = source.lower().strip()
    engine_clean = engine.lower().strip()

    if source_clean == "imdb":
        if engine_clean == "requests":
            from infrastructure.scraper.imdb_scraper import ImdbScraper
            return ImdbScraper(use_case=use_case, engine=engine_clean)

        # elif engine_clean == "playwright":
        #     from infrastructure.scraper.imdb_scraper_playwright import ImdbScraperPlaywright
        #     return ImdbScraperPlaywright(use_case=use_case, engine=engine_clean)

        else:
            raise ValueError(f"Motor '{engine_clean}' no soportado para IMDb.")

    raise ValueError(f"Source '{source}' no es reconocido.")
