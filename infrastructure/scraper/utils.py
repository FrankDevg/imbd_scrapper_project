# En: infrastructure/scraper/utils.py

import random
import time
import requests
from typing import Optional
from requests.exceptions import RequestException

from shared.config import config
from shared.logger.logging_config import setup_logger

logger = setup_logger(__name__)

def _get_headers(custom_headers: Optional[dict] = None) -> dict:
    """Combina headers base con headers personalizados si se proporcionan."""
    base_headers = {"User-Agent": random.choice(config.USER_AGENTS)}
    if custom_headers:
        base_headers.update(custom_headers)
    return base_headers

def make_request(
    url: str,
    proxy_provider,
    tor_rotator,
    method: str = "GET",
    json_payload: dict = None,
    headers: dict = None
) -> Optional[requests.Response]:
    """
    Realiza una petición HTTP robusta con soporte para GET/POST, proxies, TOR, reintentos y fallback.
    """
    
    # Define la secuencia de estrategias a intentar
    strategies = []
    if config.USE_TOR:
        strategies.append('tor')  # Si se fuerza TOR, solo se usa TOR
    else:
        strategies.append('proxy')
        strategies.append('tor')  # TOR como fallback

    for strategy in strategies:
        logger.info(f"Iniciando peticiones con estrategia: {strategy.upper()}")
        for attempt in range(1, config.MAX_RETRIES + 1):
            proxies = None
            log_ip_info = "Conexión Directa (VPN)"

            try:
                # Configura el proxy según la estrategia actual
                if strategy == 'proxy':
                    proxies = proxy_provider.get_proxy()
                    ip, city, country = proxy_provider.get_proxy_location()
                    log_ip_info = f"Proxy: {ip} ({city}, {country})"
                elif strategy == 'tor':
                    tor_rotator.rotate_ip()#BORRAR
                    
                    proxies = config.TOR_PROXY
                    ip = tor_rotator.get_current_ip()
                    log_ip_info = f"TOR: {ip}"
                
                request_headers = _get_headers(headers)
                logger.info(f"Intento {attempt}/{config.MAX_RETRIES} | {method.upper()} {url} | Usando: {log_ip_info}")

                # Realiza la petición GET o POST
                if method.upper() == 'POST':
                    response = requests.post(url, headers=request_headers, proxies=proxies, json=json_payload, timeout=config.REQUEST_TIMEOUT)
                else:
                    response = requests.get(url, headers=request_headers, proxies=proxies, timeout=config.REQUEST_TIMEOUT)
                
                logger.info(f"Respuesta: {response.status_code} | URL Final: {response.url}")

                if  response.status_code==200:
                    return response
                
                # Si estamos usando TOR y nos bloquean, rotamos la IP
                if strategy == 'tor' and response.status_code in config.BLOCK_CODES:
                    logger.warning(f"Código de bloqueo {response.status_code} con TOR. Rotando IP...")
                    tor_rotator.rotate_ip()
                    time.sleep(config.TOR_WAIT_AFTER_ROTATION)

            except RequestException as e:
                logger.warning(f"Error de red en intento {attempt} con {strategy.upper()}: {e}")
            
            # Espera antes del siguiente reintento
            time.sleep(config.RETRY_DELAYS[min(attempt - 1, len(config.RETRY_DELAYS) - 1)])
        
        # Si se completan todos los reintentos de una estrategia y no es la última, se pasa a la siguiente (fallback)
        if strategy != strategies[-1]:
            logger.warning(f"La estrategia {strategy.upper()} falló. Pasando a la siguiente...")

    logger.error(f"Todos los intentos y estrategias fallaron para la URL: {url}")
    return None