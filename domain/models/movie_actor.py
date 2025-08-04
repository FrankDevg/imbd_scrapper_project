from dataclasses import dataclass

@dataclass
class MovieActor:
    """
    Modelo que representa la relación N:M entre películas y actores.

    Esta clase actúa como tabla intermedia que vincula un actor con una película específica.

    Attributes:
        movie_id (int): Identificador de la película.
        actor_id (int): Identificador del actor.
    """
    movie_id: int
    actor_id: int
