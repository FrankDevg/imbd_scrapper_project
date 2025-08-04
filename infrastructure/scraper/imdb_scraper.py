
from bs4 import BeautifulSoup
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from domain.models import Movie, Actor
from domain.interfaces.scraper_interface import ScraperInterface
from infrastructure.scraper.utils import make_request
from shared.config import config

import logging
import requests
import re
import random

logger = logging.getLogger(__name__)

class ImdbScraper(ScraperInterface):
    """
    Scraper de películas desde IMDb que obtiene información de las películas más populares
    combinando scraping HTML y llamadas a la API GraphQL de IMDb.

    Guarda los resultados utilizando un caso de uso que persiste en CSV (u otra capa de infraestructura).
    """

    def __init__(self, use_case: SaveMovieWithActorsCsvUseCase, base_url: str = config.BASE_URL):
        """
        Constructor del scraper.

        Args:
            use_case (SaveMovieWithActorsCsvUseCase): Caso de uso para persistencia de datos.
            base_url (str): URL base de IMDb (por defecto config.BASE_URL).
        """
        self.base_url = base_url
        self.use_case = use_case
        self.total_bytes_used = 0  # Para medir el tráfico total usado

    def scrape(self, save_use_case=None) -> None:
        """
        Punto de entrada principal. Obtiene los IDs de películas y ejecuta scraping detallado
        en paralelo con ThreadPoolExecutor.
        """
        logger.info(f"Iniciando scraping desde IMDb...")

        movie_ids = self.get_combined_movie_ids()
        if not movie_ids:
            logger.error("No se pudieron obtener IDs desde HTML o GraphQL.")
            return

        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            executor.map(
                lambda indexed: self._scrape_and_save_movie_detail(indexed),
                enumerate(movie_ids[:config.NUM_MOVIES], start=1)
            )

        logger.info(f"Scraping completado.")
        logger.info(f"[TOTAL] Tráfico total usado por el scraper: {self.total_bytes_used / (1024 ** 2):.2f} MB")
        print('Tráfico total usado por el scraper: {:.2f} MB'.format(self.total_bytes_used / (1024 ** 2)))

    def _scrape_and_save_movie_detail(self, indexed_id: tuple[int, str]) -> None:
        """
        Método auxiliar que ejecuta el scraping y guarda el resultado si es válido.

        Args:
            indexed_id (tuple[int, str]): Tupla (índice, imdb_id).
        """
        movie = self._scrape_movie_detail(indexed_id)
        if movie:
            self.use_case.execute(movie)

    def _scrape_movie_detail(self, indexed_id: tuple[int, str]) -> Optional[Movie]:
        """
        Realiza el scraping del detalle de una película individual.

        Args:
            indexed_id (tuple[int, str]): Índice local e ID IMDb.

        Returns:
            Optional[Movie]: Objeto Movie con los datos parseados o None si hubo error.
        """
        movie_id_counter, imdb_id = indexed_id
        try:
            detail_path = config.TITLE_DETAIL_PATH.format(id=imdb_id)
            detail_url = self.base_url + detail_path
            detail_resp = make_request(detail_url)

            if detail_resp is None:
                return None

            detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
            self.total_bytes_used += len(detail_resp.content)

            # Datos básicos
            title_tag = detail_soup.select_one(config.SELECTORS["title"])
            year_tag = detail_soup.select_one(config.SELECTORS["year"])
            rating_tag = detail_soup.select_one(config.SELECTORS["rating"])

            title = title_tag.text.strip() if title_tag else "N/A"
            year = int(year_tag.text.strip()) if year_tag else 0
            rating = float(rating_tag.text.strip()) if rating_tag else 0.0

            # Duración en minutos
            duration = None
            for ul in detail_soup.select(config.SELECTORS["duration_container"]):
                for li in ul.select('li'):
                    dur_text = li.get_text(strip=True)
                    if "h" in dur_text or "m" in dur_text:
                        digits = [int(d) for d in re.findall(r'\d+', dur_text)]
                        if len(digits) == 2:
                            duration = digits[0] * 60 + digits[1]
                        elif len(digits) == 1:
                            duration = digits[0]
                        break
                if duration:
                    break

            # Metascore
            metascore_tag = detail_soup.select_one(config.SELECTORS["metascore"])
            metascore = int(metascore_tag.text.strip()) if metascore_tag else None

            # Actores principales (máximo 3)
            cast_tags = detail_soup.select(config.SELECTORS["actors"])
            actors = [
                Actor(id=movie_id_counter * 10 + i, name=cast.text.strip())
                for i, cast in enumerate(cast_tags[:3], start=1)
            ]

            return Movie(
                id=movie_id_counter,
                imdb_id=imdb_id,
                title=title,
                year=year,
                rating=rating,
                duration_minutes=duration,
                metascore=metascore,
                actors=actors
            )
        except Exception as e:
            logger.exception(f"Error al procesar {imdb_id}: {e}")
            return None

    def get_combined_movie_ids(self) -> List[str]:
        """
        Obtiene los IDs de las películas combinando scraping HTML y llamada GraphQL.

        Returns:
            List[str]: Lista de IDs de películas IMDb.
        """
        ids = set()

        # HTML scraping desde /chart/top/
        chart_url = config.BASE_URL + config.CHART_TOP_PATH
        resp = make_request(chart_url)
        cookies = resp.cookies if resp else None
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            html_ids = [
                a["href"].split("/")[2]
                for a in soup.select("td.titleColumn a")
                if "/title/" in a["href"]
            ]
            logger.info(f"[HTML] IDs obtenidos: {len(html_ids)}")
            ids.update(html_ids)

        # GraphQL scraping
        graphql_ids = self.fetch_graphql_ids(cookies)
        ids.update(graphql_ids)

        return list(ids)

    def fetch_graphql_ids(self, cookies: Optional[dict]) -> List[str]:
        """
        Realiza la petición GraphQL para obtener IDs adicionales de películas.

        Args:
            cookies (Optional[dict]): Cookies obtenidas de la sesión HTML, reutilizadas para autenticidad.

        Returns:
            List[str]: Lista de IMDb IDs obtenidos desde la API GraphQL.
        """
        try:
            headers = {
                "User-Agent": random.choice(config.USER_AGENTS),
                "Accept": "application/graphql+json, application/json",
                "Content-Type": "application/json"
            }

            payload = {
                "operationName": config.GRAPHQL_OPERATION,
                "variables": {
                    "first": config.NUM_MOVIES,
                    "isInPace": False,
                    "locale": config.GRAPHQL_LOCALE
                },
                "extensions": {
                    "persistedQuery": {
                        "sha256Hash": config.GRAPHQL_HASH,
                        "version": config.GRAPHQL_VERSION
                    }
                }
            }

            proxies = config.TOR_PROXY if config.USE_TOR else None

            resp = requests.post(
                config.GRAPHQL_URL,
                headers=headers,
                cookies=cookies,
                json=payload,
                proxies=proxies,
                timeout=config.REQUEST_TIMEOUT
            )

            if resp.status_code == 200:
                data = resp.json()
                edges = data.get("data", {}).get("chartTitles", {}).get("edges", [])
                ids = [edge["node"]["id"] for edge in edges if edge.get("node", {}).get("id")]
                logger.info(f"[GraphQL] IDs obtenidos: {len(ids)}")
                return ids
            else:
                logger.warning(f"[GraphQL] Status: {resp.status_code} Body: {resp.text}")
        except Exception as e:
            logger.error(f"[GraphQL] Error: {e}")
        return []
