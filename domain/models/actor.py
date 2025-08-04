from dataclasses import dataclass
from typing import Optional

@dataclass
class Actor:
    """
    Modelo de dominio que representa un actor dentro del sistema.

    Attributes:
        id (int): Identificador único del actor.
        name (str): Nombre del actor.
    """
    id: int
    name: str
