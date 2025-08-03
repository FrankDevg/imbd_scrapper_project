import csv
import os
import threading
from typing import List
from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository

ACTORS_CSV = "data/actors.csv"
ACTOR_HEADERS = ["id", "movie_id", "name"]
actor_lock = threading.Lock()

class ActorCsvRepository(ActorRepository):
    def __init__(self):
        os.makedirs(os.path.dirname(ACTORS_CSV), exist_ok=True)
        if not os.path.exists(ACTORS_CSV):
            with open(ACTORS_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(ACTOR_HEADERS)

    def save(self, actor: Actor) -> None:
        with actor_lock:
            with open(ACTORS_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    actor.id,
                    actor.name
                ])