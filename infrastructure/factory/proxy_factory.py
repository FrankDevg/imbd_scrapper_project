# infrastructure/network/proxy_provider_factory.py

from domain.interfaces.proxy_interface import ProxyProviderInterface
from infrastructure.provider.proxy_provider import ProxyProvider

def get_proxy_provider() -> ProxyProviderInterface:
    """
    Fábrica que retorna una instancia concreta del proveedor de proxy.

    Esta función desacopla la creación del objeto ProxyProvider de su uso,
    permitiendo mayor flexibilidad en pruebas o futuras implementaciones.

    Returns:
        ProxyProviderInterface: Instancia que implementa la lógica de provisión de proxy.
    """
    return ProxyProvider()
