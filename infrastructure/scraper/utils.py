import random
import time
import requests
from typing import Optional
from requests.exceptions import RequestException

from shared.config import config
from shared.logger.logging_config import setup_logger

logger = setup_logger(__name__)

def _get_headers():
    return {
        "User-Agent": random.choice(config.USER_AGENTS)
    }

def _log_status(response: requests.Response):
    logger.info(f"[STATUS CODE] {response.status_code} | Final URL: {response.url}")

def _should_rotate_tor(status_code: int) -> bool:
    return status_code in config.BLOCK_CODES

def _request_with_proxy(url: str, attempt: int, proxy_provider) -> Optional[requests.Response]:
    headers = _get_headers()
    proxies = proxy_provider.get_proxy()
    ip, city, country = proxy_provider.get_proxy_location()
    logger.info(f"[Proxy Attempt {attempt}] GET {url} | IP: {ip} | {city}, {country} | UA: {headers['User-Agent']}")
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=config.REQUEST_TIMEOUT)
        _log_status(response)
        if 200 <= response.status_code < 300:
            return response
    except RequestException as e:
        logger.error(f"[ERROR] Proxy request failed: {e}")
    return None

def _request_with_tor(
    url: str,
    attempt: int,
    tor_rotator,
    allow_rotation: bool = True,
    method: str = "GET",
    json_payload: Optional[dict] = None,
    headers: Optional[dict] = None
) -> Optional[requests.Response]:
    headers = headers or _get_headers()
    proxies = config.TOR_PROXY
    ip = tor_rotator.get_current_ip()
    logger.info(f"[TOR Attempt {attempt}] {method} {url} | IP: {ip} | UA: {headers['User-Agent']}")
    try:
        logger.info(f"[TOR] Usando proxy: {proxies}")

        if method.upper() == "POST":
            response = requests.post(
                url,
                headers=headers,
                proxies=proxies,
                json=json_payload,
                timeout=config.REQUEST_TIMEOUT
            )
        else:
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=config.REQUEST_TIMEOUT
            )

        _log_status(response)

        if response.status_code == 200:
            return response
        elif _should_rotate_tor(response.status_code) and allow_rotation:
            logger.warning(f"[TOR] Código {response.status_code} recibido. Rotando IP TOR...")
            tor_rotator.rotate_ip()
            time.sleep(config.TOR_WAIT_AFTER_ROTATION)
            return _request_with_tor(
                url,
                attempt + 1,
                tor_rotator,
                allow_rotation=False,
                method=method,
                json_payload=json_payload,
                headers=headers
            )

    except RequestException as e:
        logger.error(f"[ERROR] TOR request failed: {e}")
    return None

def make_request(
    url: str,
    proxy_provider,
    tor_rotator,
    method: str = "GET",
    json_payload: dict = None,
    headers: dict = None,
    max_retries: int = None
) -> Optional[requests.Response]:
    """
    Hace una petición HTTP robusta con soporte para GET/POST, proxies, TOR y reintentos.

    Args:
        url (str): URL a la que se hace la petición.
        proxy_provider: Proveedor de proxy (inyectado).
        tor_rotator: Manejador de TOR (inyectado).
        method (str): 'GET' o 'POST'.
        json_payload (dict): Payload para POST.
        headers (dict): Headers personalizados.
        max_retries (int): Número máximo de reintentos.

    Returns:
        Optional[requests.Response]: Respuesta exitosa o None si falla.
    """
    retries = max_retries or config.MAX_RETRIES
    delay_list = config.RETRY_DELAYS

    def _send_request(session, method, url, **kwargs):
        return session.post(url, **kwargs) if method.upper() == "POST" else session.get(url, **kwargs)

    # Paso 1: Intentos con proxy personalizado 
    if not config.USE_TOR:
        for attempt in range(1, retries + 1):
            try:
                proxy = proxy_provider.get_proxy()
                session = requests.Session()

                request_headers = headers.copy() if headers else {}
                request_headers["User-Agent"] = random.choice(config.USER_AGENTS)

                logger.info(f"[ATTEMPT {attempt}] Con proxy: {proxy}")

                response = _request_with_proxy(url, attempt, proxy_provider)

                if response and response.status_code == 200:
                    return response

            except Exception as e:
                logger.warning(f"[PROXY] Intento {attempt} fallido: {e}")
                time.sleep(delay_list[min(attempt - 1, len(delay_list) - 1)])

    # Paso 2: Fallback con TOR (si falla el proxy o se fuerza TOR)
    logger.warning("[FALLBACK] Probando con TOR...")
    for attempt in range(1, retries + 1):
        try:
            response = _request_with_tor(
                url=url,
                attempt=attempt,
                tor_rotator=tor_rotator,
                allow_rotation=True,
                method=method,
                json_payload=json_payload,
                headers=headers
            )

            if response and response.status_code == 200:
                return response

        except Exception as e:
            logger.warning(f"[TOR] Intento {attempt} fallido: {e}")
            time.sleep(delay_list[min(attempt - 1, len(delay_list) - 1)])

    logger.error(f"[ERROR] Todos los intentos fallaron para → {url}")
    return None
