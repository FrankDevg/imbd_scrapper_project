
import random
import requests
import logging
from typing import Optional, Dict
from domain.interfaces.proxy_interface import ProxyProviderInterface
from shared.config import config

logger = logging.getLogger(__name__)

class ProxyProvider(ProxyProviderInterface):
    """
    Implementación del proveedor de proxy que selecciona dinámicamente el tipo de proxy a utilizar.

    Soporta:
    - Proxy autenticado personalizado
    - Red TOR
    - Lista rotativa de proxies
    - Conexión directa (sin proxy)
    """
    def __init__(self):
        self.current_proxy: Optional[Dict[str, str]] = None
        
    def get_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retorna la configuración de proxy a utilizar según la prioridad:

        1. Proxy autenticado (usuario/clave)
        2. Red TOR
        3. Proxy aleatorio desde lista
        4. Conexión directa (None)

        Returns:
            Optional[Dict[str, str]]: Diccionario con configuración de proxy para requests, o None.
        """
        proxy_to_use = None # Variable para almacenar la decisión

        if config.USE_CUSTOM_PROXY:
            proxy_auth = f"{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_HOST}:{config.PROXY_PORT}"
            logger.info(f"[PROXY] Usando proxy autenticado: {config.PROXY_HOST}:{config.PROXY_PORT}")
            proxy_to_use = {
                "http": f"http://{proxy_auth}",
                "https": f"http://{proxy_auth}"
            }
        elif config.USE_TOR:
            logger.info(f"[PROXY] Usando red TOR: {config.TOR_PROXY}")
            proxy_to_use = config.TOR_PROXY
        elif hasattr(config, 'PROXY_LIST') and config.PROXY_LIST:
            selected = random.choice(config.PROXY_LIST)
            logger.info(f"[PROXY] Usando proxy de lista: {selected['http']}")
            proxy_to_use = selected
        else:
            logger.warning("[PROXY] No se encontró proxy configurado. Usando conexión directa.")
            proxy_to_use = None

        self.current_proxy = proxy_to_use
        
        return self.current_proxy

    def get_proxy_location(self) -> tuple[str, str, str]:
        """
        Consulta la IP pública, ciudad y país asociada al proxy proporcionado, usando el servicio ipinfo.io.

        Args:
            proxy (Optional[Dict[str, str]]): Proxy con el cual realizar la consulta.

        Returns:
            tuple[str, str, str]: (IP pública, ciudad, país). Si hay error, retorna ('N/A', 'N/A', 'N/A').
        """
        try:
            resp = requests.get(config.URL_IPINFO, proxies=self.current_proxy, timeout=config.REQUEST_TIMEOUT)
            resp.raise_for_status()

            data = resp.json()
            ip = data.get("ip", "N/A")
            city = data.get("city", "N/A")
            country = data.get("country", "N/A")
            return ip, city, country
        except requests.exceptions.RequestException as e:
            logger.warning(f"[PROXY INFO] No se pudo obtener IP pública: {e}")
        
        return "N/A", "N/A", "N/A"
