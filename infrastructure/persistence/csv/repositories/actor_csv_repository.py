# En: infrastructure/persistence/csv/repositories/actor_csv_repository.py

import csv
import os
import threading
from typing import Optional, List
from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository

ACTORS_CSV = "data/actors.csv"
ACTOR_HEADERS = ["id", "name"]
actor_lock = threading.Lock()

class ActorCsvRepository(ActorRepository):
    """
    Implementación del repositorio de actores para almacenamiento en archivos CSV.
    """
    def __init__(self):
        os.makedirs(os.path.dirname(ACTORS_CSV), exist_ok=True)
        if not os.path.exists(ACTORS_CSV):
            with open(ACTORS_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(ACTOR_HEADERS)
    
    def _get_next_id(self) -> int:
        """Lee el CSV para determinar el siguiente ID disponible."""
        with open(ACTORS_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) # Saltar encabezados
            last_id = 0
            for row in reader:
                if row:
                    last_id = int(row[0])
            return last_id + 1

    def save(self, actor: Actor) -> Actor:
        """
        Guarda un actor en CSV, asignándole un nuevo ID si no lo tiene.
        Retorna el actor con el ID asignado.
        """
        with actor_lock:
            if actor.id is None:
                actor.id = self._get_next_id()
            
            with open(ACTORS_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([actor.id, actor.name])
            
            return actor

    def find_by_name(self, name: str) -> Optional[Actor]:
        """
        Busca un actor por su nombre en el archivo CSV.
        """
        with actor_lock:
            with open(ACTORS_CSV, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["name"].lower() == name.lower():
                        return Actor(id=int(row["id"]), name=row["name"])
        return None