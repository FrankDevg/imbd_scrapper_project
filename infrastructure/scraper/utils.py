# infrastructure/scraper/utils.py

import time
import requests
from typing import Optional
from requests.exceptions import RequestException
from shared.config import config
from shared.logger.logging_config import setup_logger
from infrastructure.scraper.network_utils import get_random_user_agent, get_proxy

logger = setup_logger(__name__)

def make_request(url: str, use_tor: bool = False) -> Optional[requests.Response]:
    """
    Realiza una petición HTTP a la URL dada, con rotación de User-Agent y soporte opcional para proxy TOR.
    Reintenta automáticamente con delay si hay error de red o status inesperado.
    """
    for attempt, delay in zip(range(1, config.MAX_RETRIES + 1), config.RETRY_DELAYS):
        try:
            headers = {"User-Agent": get_random_user_agent()}
            proxy = get_proxy(use_tor=use_tor)

            logger.info(f"[Attempt {attempt}] GET {url} | Proxy: {'TOR' if use_tor else 'None'} | UA: {headers['User-Agent']}")

            response = requests.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=config.REQUEST_TIMEOUT
            )

            logger.info(f"[STATUS CODE] {response.status_code} | Final URL: {response.url}")

            if response.status_code in [200, 202]:
                return response
            else:
                logger.warning(f"[WARNING] Respuesta inesperada: HTTP {response.status_code}")

        except RequestException as e:
            logger.error(f"[❌ ERROR] Request fallida a {url}: {e}")

        time.sleep(delay)

    logger.error(f"[❌ ERROR] Fallo total tras {config.MAX_RETRIES} intentos → {url}")
    return None
