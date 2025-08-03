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
    def __init__(self):
        os.makedirs(os.path.dirname(MOVIE_ACTOR_CSV), exist_ok=True)
        if not os.path.exists(MOVIE_ACTOR_CSV):
            with open(MOVIE_ACTOR_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(MOVIE_ACTOR_HEADERS)

    def save(self, relation: MovieActor) -> None:
        with relation_lock:
            with open(MOVIE_ACTOR_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    relation.movie_id,
                    relation.actor_id
                ])
