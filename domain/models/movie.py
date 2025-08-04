from dataclasses import dataclass
from typing import Optional, List
from domain.models.actor import Actor

@dataclass
class Movie:
    """
    Modelo de dominio que representa una película extraída del scraping.

    Attributes:
        id (Optional[int]): ID único interno (puede ser asignado por la base de datos).
        imdb_id (str): Identificador de la película en IMDb (por ejemplo, 'tt0111161').
        title (str): Título de la película.
        year (int): Año de estreno.
        rating (float): Calificación promedio de usuarios en IMDb.
        duration_minutes (Optional[int]): Duración de la película en minutos.
        metascore (Optional[int]): Puntuación de Metacritic (0 a 100), si está disponible.
        actors (List[Actor]): Lista de actores principales asociados a la película.
    """
    id: Optional[int]
    imdb_id: str         
    title: str
    year: int
    rating: float
    duration_minutes: Optional[int]
    metascore: Optional[int]
    actors: List[Actor]
