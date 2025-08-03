from dataclasses import dataclass
from typing import Optional, List
from domain.models.actor import Actor

@dataclass
class Movie:
    id: int
    title: str
    year: int
    rating: float
    duration_minutes: Optional[int]
    metascore: Optional[int]
    actors: List[Actor]
