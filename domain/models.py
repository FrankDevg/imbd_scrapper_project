from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Actor:
    id: int
    name: str
    movie_id: int  # Relación con la película

@dataclass
class Movie:
    id: int
    title: str
    year: int
    rating: float
    duration_minutes: Optional[int]
    metascore: Optional[int]
    actors: List[Actor]  # Lista de actores asociados
