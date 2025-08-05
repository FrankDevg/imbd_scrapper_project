# En: domain/models/movie_actor.py

from dataclasses import dataclass

@dataclass
class MovieActor:
    """
    Modelo que representa la relación N:M y valida su integridad.
    """
    movie_id: int
    actor_id: int

    def __post_init__(self):
        """Valida los datos de la relación después de la inicialización."""
        if not isinstance(self.movie_id, int) or self.movie_id <= 0:
            raise ValueError("movie_id debe ser un entero positivo.")
        
        if not isinstance(self.actor_id, int) or self.actor_id <= 0:
            raise ValueError("actor_id debe ser un entero positivo.")