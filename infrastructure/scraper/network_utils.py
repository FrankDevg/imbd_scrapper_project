# infrastructure/scraper/network_utils.py

import random
from typing import Optional, Dict
from shared.config import config

def get_random_user_agent() -> str:
    """
    Devuelve un User-Agent aleatorio desde la configuración.
    """
    return random.choice(config.USER_AGENTS)

def get_proxy(use_tor: bool = False) -> Optional[Dict[str, str]]:
    """
    Retorna un diccionario con el proxy adecuado.
    """
    if use_tor:
        return config.TOR_PROXY
    if hasattr(config, 'PROXY_LIST') and config.PROXY_LIST:
        return random.choice(config.PROXY_LIST)
    return None
