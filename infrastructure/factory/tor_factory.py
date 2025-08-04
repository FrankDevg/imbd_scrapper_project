from infrastructure.proxy_rotation.tor_rotator import TorRotator
from domain.interfaces.tor_interface import TorInterface

def get_tor_rotator() -> TorInterface:
    return TorRotator()
