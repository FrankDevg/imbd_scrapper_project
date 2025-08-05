import logging
import re
import random
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

from domain.models import Movie, Actor
from domain.interfaces.scraper_interface import ScraperInterface
from domain.interfaces.use_case_interface import UseCaseInterface
from domain.interfaces.proxy_interface import ProxyProviderInterface
from domain.interfaces.tor_interface import TorInterface
from infrastructure.scraper.utils import make_request
from shared.config import config

logger = logging.getLogger(__name__)

class ImdbScraper(ScraperInterface):
    """
    Scraper de películas desde IMDb con soporte para proxies, TOR, y persistencia desacoplada.
    """

    def __init__(
        self,
        use_case: UseCaseInterface,
        proxy_provider: ProxyProviderInterface,
        tor_rotator: TorInterface,
        engine: str,
        base_url: str = config.BASE_URL
    ):
        self.use_case = use_case
        self.proxy_provider = proxy_provider
        self.tor_rotator = tor_rotator
        self.engine = engine
        self.base_url = base_url
        self.total_bytes_used = 0

    def scrape(self) -> None:
        logger.info("Iniciando scraping desde IMDb...")
        movie_ids = self._get_combined_movie_ids()
        if not movie_ids:
            logger.error("No se pudieron obtener IDs de películas.")
            return

        with ThreadPoolExecutor(max_workers=config.MAX_THREADS) as executor:
            executor.map(
                self._scrape_and_save_movie_detail,
                enumerate(movie_ids[:config.NUM_MOVIES], start=1)
            )

        logger.info("Scraping completado.")
        logger.info(f"Tráfico total usado: {self.total_bytes_used / (1024 ** 2):.2f} MB")

    def _scrape_and_save_movie_detail(self, indexed_id: tuple[int, str]) -> None:
        imdb_id = indexed_id[1]
        try:
            movie = self._scrape_movie_detail(indexed_id)
            if movie:
                self.use_case.execute(movie)
        except Exception as e:
            logger.error(f"Error inesperado al procesar {imdb_id}: {e}", exc_info=True)

    def _scrape_movie_detail(self, indexed_id: tuple[int, str]) -> Optional[Movie]:
        movie_id_counter, imdb_id = indexed_id
        detail_url = self.base_url + config.TITLE_DETAIL_PATH.format(id=imdb_id)

        response = make_request(
            url=detail_url,
            proxy_provider=self.proxy_provider,
            tor_rotator=self.tor_rotator
        )

        if not response:
            logger.warning(f"No se pudo obtener respuesta para la URL: {detail_url}")
            return None

        self.total_bytes_used += len(response.content)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.select_one(config.SELECTORS["title"]).text.strip() if soup.select_one(config.SELECTORS["title"]) else ""
        year_tag = soup.select_one(config.SELECTORS["year"])
        year_str = year_tag.text.strip("()") if year_tag else "0"
        year = int(re.search(r'\d{4}', year_str).group()) if re.search(r'\d{4}', year_str) else 0
        rating = float(soup.select_one(config.SELECTORS["rating"]).text.strip()) if soup.select_one(config.SELECTORS["rating"]) else 0.0
        metascore_tag = soup.select_one(config.SELECTORS["metascore"])
        metascore = int(metascore_tag.text.strip()) if metascore_tag else None

        # Duración en minutos
        duration = None
        ul_list = soup.select(config.SELECTORS.get("duration_container", ""))
        for ul in ul_list:
            for li in ul.find_all("li"):
                text = li.get_text(strip=True).lower()
                if re.search(r"\d+h|\d+m", text):
                    digits = [int(d) for d in re.findall(r"\d+", text)]
                    if "h" in text and "m" in text and len(digits) == 2:
                        duration = digits[0] * 60 + digits[1]
                    elif "h" in text and len(digits) == 1:
                        duration = digits[0] * 60
                    elif "m" in text and len(digits) == 1:
                        duration = digits[0]
                    break
            if duration:
                break


        cast_tags = soup.select(config.SELECTORS["actors"])[:3]
        actors = [
            Actor(id=None, name=cast.text.strip())
            for cast in cast_tags if cast.text.strip()
        ]

        return Movie(
            id=None,
            imdb_id=imdb_id,
            title=title,
            year=year,
            rating=rating,
            duration_minutes=duration,
            metascore=metascore,
            actors=actors
        )

    def _get_combined_movie_ids(self) -> List[str]:
        ids = set()
        chart_url = self.base_url + config.CHART_TOP_PATH

        response = make_request(
            url=chart_url,
            proxy_provider=self.proxy_provider,
            tor_rotator=self.tor_rotator
        )

        cookies = response.cookies if response else None
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            html_ids = [
                a["href"].split("/")[2]
                for a in soup.select("td.titleColumn a")
                if "/title/" in a["href"]
            ]
            logger.info(f"[HTML] IDs obtenidos: {len(html_ids)}")
            ids.update(html_ids)

        graphql_ids = self._fetch_graphql_ids(cookies)
        ids.update(graphql_ids)

        return list(ids)

    def _fetch_graphql_ids(self, cookies: Optional[dict]) -> List[str]:
        logger.info("Obteniendo IDs adicionales desde GraphQL...")
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

            response = make_request(
                url=config.GRAPHQL_URL,
                proxy_provider=self.proxy_provider,
                tor_rotator=self.tor_rotator,
                method="POST",
                json_payload=payload,
                headers=headers
            )

            if response:
                data = response.json()
                edges = data.get("data", {}).get("chartTitles", {}).get("edges", [])
                ids = [edge["node"]["id"] for edge in edges if edge.get("node", {}).get("id")]
                logger.info(f"[GraphQL] IDs obtenidos: {len(ids)}")
                return ids
            else:
                logger.warning("[GraphQL] No se pudo obtener respuesta válida.")
        except Exception as e:
            logger.error(f"[GraphQL] Error al procesar la respuesta: {e}")

        return []
