from infrastructure.proxy_rotation.tor_rotator import TorRotator
from domain.interfaces.tor_interface import TorInterface

def get_tor_rotator() -> TorInterface:
    """
    Fábrica que retorna una instancia concreta del rotador de IP para la red TOR.

    Esta función permite desacoplar la creación del rotador de su uso,
    facilitando pruebas y cambios de implementación.

    Returns:
        TorInterface: Instancia que implementa la rotación y consulta de IP TOR.
    """
    return TorRotator()
