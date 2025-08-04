# infrastructure/network/proxy_provider_factory.py

from domain.interfaces.proxy_interface import ProxyProviderInterface
from infrastructure.provider.proxy_provider import ProxyProvider

def get_proxy_provider() -> ProxyProviderInterface:
    """
    Devuelve una instancia del proveedor de proxy a utilizar.
    """
    return ProxyProvider()
