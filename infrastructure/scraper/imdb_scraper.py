# infrastructure/scraper/imdb_scraper.py

from bs4 import BeautifulSoup
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from domain.models import Movie, Actor
from domain.scraper_interface import ScraperInterface
from infrastructure.scraper.utils import make_request
from shared.config import config
from infrastructure.scraper.network_utils import get_random_user_agent

import logging
import os
import json
import requests
import re

logger = logging.getLogger(__name__)

class ImdbScraper(ScraperInterface):
    def __init__(self,use_case: SaveMovieWithActorsCsvUseCase,  base_url: str = config.BASE_URL):
        self.base_url = base_url
        self.use_case = use_case
    def scrape(self, save_use_case=None) -> None:
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

    def _scrape_and_save_movie_detail(self, indexed_id: tuple[int, str]) -> None:
        movie = self._scrape_movie_detail(indexed_id)
        if movie:
            self.use_case.execute(movie)

    def _scrape_movie_detail(self, indexed_id: tuple[int, str]) -> Optional[Movie]:
        movie_id_counter, imdb_id = indexed_id
        try:
            detail_path = config.TITLE_DETAIL_PATH.format(id=imdb_id)
            detail_url = self.base_url + detail_path
            detail_resp = make_request(detail_url, use_tor=config.USE_TOR)

            if detail_resp is None:
                return None

            detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

            title_tag = detail_soup.select_one(config.SELECTORS["title"])
            year_tag = detail_soup.select_one(config.SELECTORS["year"])
            rating_tag = detail_soup.select_one(config.SELECTORS["rating"])
            title = title_tag.text.strip() if title_tag else "N/A"
            year = int(year_tag.text.strip()) if year_tag else 0
            rating = float(rating_tag.text.strip()) if rating_tag else 0.0

            # Duración
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

            metascore_tag = detail_soup.select_one(config.SELECTORS["metascore"])
            metascore = int(metascore_tag.text.strip()) if metascore_tag else None

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
        ids = set()

        # HTML
        chart_url = config.BASE_URL + config.CHART_TOP_PATH
        resp = make_request(chart_url, use_tor=config.USE_TOR)
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

        # GraphQL
        try:
            headers = {
                "User-Agent": get_random_user_agent(),
                "Accept": "application/graphql+json, application/json",
                "Content-Type": "application/json"
            }
            resp_graphql = requests.post(
                config.GRAPHQL_URL,
                headers=headers,
                cookies=cookies,
                json={
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
                },
                proxies=config.TOR_PROXY if config.USE_TOR else None,
                timeout=config.REQUEST_TIMEOUT
            )
            
            if resp_graphql.status_code == 200:
                data = resp_graphql.json()
                edges = data.get("data", {}).get("chartTitles", {}).get("edges", [])
                graphql_ids = [edge["node"]["id"] for edge in edges if edge.get("node", {}).get("id")]
                logger.info(f"[GraphQL] IDs obtenidos: {len(graphql_ids)}")
                ids.update(graphql_ids)
            else:
                logger.warning(f"[GraphQL] Status: {resp_graphql.status_code} Body: {resp_graphql.text}")
        except Exception as e:
            logger.error(f"[GraphQL] Error: {e}")

        return list(ids)
