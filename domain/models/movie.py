# En: domain/models/movie.py

from dataclasses import dataclass, field
from typing import Optional, List
import re
from domain.models.actor import Actor

@dataclass
class Movie:
    """
    Modelo de dominio que representa una película y valida su propia integridad.
    """
    id: Optional[int]
    imdb_id: str
    title: str
    year: int
    rating: float
    duration_minutes: Optional[int]
    metascore: Optional[int]
    actors: List[Actor] = field(default_factory=list)

    def __post_init__(self):
        """
        Realiza validaciones en los datos después de que el objeto es creado.
        """
        # Limpieza de datos
        self.title = self.title.strip()
        self.imdb_id = self.imdb_id.strip()

        # Reglas de validación
        if not re.match(r"^tt\d{7,}$", self.imdb_id):
            raise ValueError(f"IMDb ID inválido: '{self.imdb_id}'")
        if not self.title:
            raise ValueError("El título no puede estar vacío.")
        if not (1888 <= self.year <= 2030):
            raise ValueError(f"Año inválido: {self.year}. Debe estar entre 1888 y 2030.")
        if not (0.0 <= self.rating <= 10.0):
            raise ValueError(f"Rating inválido: {self.rating}. Debe estar entre 0.0 y 10.0.")
        if self.duration_minutes is not None and self.duration_minutes <= 0:
            raise ValueError(f"La duración debe ser un número positivo.")
        if self.metascore is not None and not (0 <= self.metascore <= 100):
            raise ValueError(f"Metascore inválido: {self.metascore}. Debe estar entre 0 y 100.")