import csv
import os
import threading
from typing import List
from domain.models.movie_actor import MovieActor
from domain.repositories.movie_actor_repository import MovieActorRepository

MOVIE_ACTOR_CSV = "data/movie_actor.csv"
MOVIE_ACTOR_HEADERS = ["movie_id", "actor_id"]
relation_lock = threading.Lock()

class MovieActorCsvRepository(MovieActorRepository):
    """
    Implementación del repositorio para guardar relaciones N:M en un archivo CSV.
    """
    def __init__(self):
        os.makedirs(os.path.dirname(MOVIE_ACTOR_CSV), exist_ok=True)
        if not os.path.exists(MOVIE_ACTOR_CSV):
            with open(MOVIE_ACTOR_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(MOVIE_ACTOR_HEADERS)

    def save(self, relation: MovieActor) -> None:
        """
        Guarda una única relación película-actor en el archivo CSV.
        """
        with relation_lock:
            with open(MOVIE_ACTOR_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([relation.movie_id, relation.actor_id])

    def save_many(self, relations: List[MovieActor]) -> None:
        """
        Guarda una lista de relaciones película-actor de forma eficiente usando writerows.
        """
        with relation_lock:
            with open(MOVIE_ACTOR_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                rows_to_write = [(rel.movie_id, rel.actor_id) for rel in relations]
                writer.writerows(rows_to_write)