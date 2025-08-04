import random
import time
import requests
from typing import Optional
from requests.exceptions import RequestException

from shared.config import config
from shared.logger.logging_config import setup_logger
from infrastructure.factory.proxy_factory import get_proxy_provider
from infrastructure.factory.tor_factory import get_tor_rotator 

logger = setup_logger(__name__)
proxy_provider = get_proxy_provider()
tor_rotator = get_tor_rotator()

def _get_headers():
    """
    Genera un header HTTP aleatorio con User-Agent rotativo.
    
    Returns:
        dict: Cabeceras con User-Agent aleatorio.
    """
    return {
        "User-Agent": random.choice(config.USER_AGENTS)
    }

def _log_status(response: requests.Response):
    """
    Loguea el código de estado y la URL final de una respuesta HTTP.

    Args:
        response (requests.Response): Respuesta HTTP obtenida.
    """
    logger.info(f"[STATUS CODE] {response.status_code} | Final URL: {response.url}")

def _should_rotate_tor(status_code: int) -> bool:
    """
    Determina si se debe rotar la IP TOR según el código de estado.

    Args:
        status_code (int): Código de estado HTTP recibido.

    Returns:
        bool: True si se debe rotar IP, False caso contrario.
    """
    return status_code in config.BLOCK_CODES

def _request_with_proxy(url: str, attempt: int) -> Optional[requests.Response]:
    """
    Realiza una solicitud HTTP usando un proxy obtenido del proveedor.

    Args:
        url (str): URL a consultar.
        attempt (int): Número de intento.

    Returns:
        Optional[requests.Response]: Respuesta HTTP o None si falla.
    """
    headers = _get_headers()
    proxies = proxy_provider.get_proxy()
    ip, city, country = proxy_provider.get_proxy_location(proxies)
    logger.info(f"[Proxy Attempt {attempt}] GET {url} | IP: {ip} | {city}, {country} | UA: {headers['User-Agent']}")

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=config.REQUEST_TIMEOUT)
        _log_status(response)
        if response.status_code == 200:
            return response
    except RequestException as e:
        logger.error(f"[ERROR] Proxy request failed: {e}")
    return None

def _request_with_tor(url: str, attempt: int, allow_rotation: bool = True) -> Optional[requests.Response]:
    """
    Realiza una solicitud HTTP usando TOR, y rota IP si se detecta bloqueo.

    Args:
        url (str): URL a consultar.
        attempt (int): Número de intento actual.
        allow_rotation (bool): Si se permite una única rotación de IP TOR.

    Returns:
        Optional[requests.Response]: Respuesta HTTP o None si falla.
    """
    headers = _get_headers()
    proxies = config.TOR_PROXY
    ip = tor_rotator.get_current_ip()
    logger.info(f"[TOR Attempt {attempt}] GET {url} | IP: {ip} | UA: {headers['User-Agent']}")

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=config.REQUEST_TIMEOUT)
        _log_status(response)

        if response.status_code == 200:
            return response
        elif _should_rotate_tor(response.status_code) and allow_rotation:
            logger.warning(f"[TOR] Código {response.status_code} recibido. Rotando IP TOR...")
            tor_rotator.rotate_ip()
            time.sleep(config.TOR_WAIT_AFTER_ROTATION)
            return _request_with_tor(url, attempt + 1, allow_rotation=False)  # evita bucles infinitos

    except RequestException as e:
        logger.error(f"[ERROR] TOR request failed: {e}")
    return None

def make_request(url: str) -> Optional[requests.Response]:
    """
    Realiza una solicitud HTTP con soporte para TOR y proxies, aplicando lógica de reintentos.

    Flujo de prioridad:
        - Si config.USE_TOR = True → intenta 3 veces con TOR.
        - Si config.USE_TOR = False → intenta 3 veces con proxy, luego 3 veces con TOR como fallback.

    Args:
        url (str): URL a consultar.

    Returns:
        Optional[requests.Response]: Respuesta HTTP válida o None si todos los intentos fallan.
    """
    retries = config.MAX_RETRIES

    if config.USE_TOR:
        for attempt in range(1, retries + 1):
            response = _request_with_tor(url, attempt)
            if response and response.status_code == 200:
                return response
            time.sleep(config.RETRY_DELAYS[min(attempt - 1, len(config.RETRY_DELAYS) - 1)])

        logger.error(f"[TOR ERROR] Todos los intentos con TOR fallaron → {url}")
        return None

    # Intentos con proxy
    for attempt in range(1, retries + 1):
        response = _request_with_proxy(url, attempt)
        if response and response.status_code == 200:
            return response
        time.sleep(config.RETRY_DELAYS[min(attempt - 1, len(config.RETRY_DELAYS) - 1)])

    # Fallback a TOR si falla el proxy
    logger.warning("[FALLBACK] Todos los intentos con proxy fallaron. Probando con TOR...")

    for attempt in range(1, retries + 1):
        response = _request_with_tor(url, attempt)
        if response and response.status_code == 200:
            return response
        time.sleep(config.RETRY_DELAYS[min(attempt - 1, len(config.RETRY_DELAYS) - 1)])

    logger.error(f"[ERROR] Proxy y TOR fallaron → {url}")
    return None
