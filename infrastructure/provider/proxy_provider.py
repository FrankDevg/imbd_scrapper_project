# infrastructure/network/proxy_provider.py

import random
import requests
import logging
from typing import Optional, Dict
from domain.interfaces.proxy_interface import ProxyProviderInterface
from shared.config import config

logger = logging.getLogger(__name__)

class ProxyProvider(ProxyProviderInterface):
    def get_proxy(self) -> Optional[Dict[str, str]]:
        if config.USE_CUSTOM_PROXY:
            proxy_auth = f"{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}"
            logger.info(f"[PROXY] Usando proxy autenticado: {config.PROXY_HOST}:{config.PROXY_PORT}")
            return {
                "http": f"http://{proxy_auth}",
                "https": f"http://{proxy_auth}"
            }

        if config.USE_TOR:
            logger.info(f"[PROXY] Usando red TOR: {config.TOR_PROXY}")
            return config.TOR_PROXY

        if hasattr(config, 'PROXY_LIST') and config.PROXY_LIST:
            selected = random.choice(config.PROXY_LIST)
            logger.info(f"[PROXY] Usando proxy de lista: {selected['http']}")
            return selected

        logger.warning("[PROXY] No se encontró proxy válido. Usando conexión directa (sin proxy).")
        return None

    def get_proxy_location(self, proxy: Optional[Dict[str, str]]) -> tuple[str, str, str]:
        try:
            resp = requests.get("https://ipinfo.io/json", proxies=proxy, timeout=config.REQUEST_TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                ip = data.get("ip", "N/A")
                city = data.get("city", "N/A")
                country = data.get("country", "N/A")
                return ip, city, country
        except Exception as e:
            logger.warning(f"[PROXY INFO] No se pudo obtener IP pública: {e}")
        return "N/A", "N/A", "N/A"
