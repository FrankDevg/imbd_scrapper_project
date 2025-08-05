# En: domain/models/actor.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class Actor:
    """
    Modelo de dominio que representa un actor y valida su propia integridad.
    """
    id: Optional[int]
    name: str

    def __post_init__(self):
        """Valida los datos del actor después de la inicialización."""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("El nombre del actor no puede estar vacío.")