import csv
import os
import threading
from typing import List
from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository

ACTORS_CSV = "data/actors.csv"
ACTOR_HEADERS = ["id",  "name"] 
actor_lock = threading.Lock()

class ActorCsvRepository(ActorRepository):
    """
    Implementación del repositorio de actores para almacenamiento en archivos CSV.

    Este repositorio garantiza que el archivo `actors.csv` exista, y proporciona
    una operación de guardado segura con bloqueo por hilo para entornos concurrentes.
    """

    def __init__(self):
        """
        Inicializa el repositorio, asegurando la existencia del directorio y archivo CSV
        con los encabezados definidos.
        """
        os.makedirs(os.path.dirname(ACTORS_CSV), exist_ok=True)
        if not os.path.exists(ACTORS_CSV):
            with open(ACTORS_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(ACTOR_HEADERS)

    def save(self, actor: Actor) -> None:
        """
        Guarda un actor en el archivo CSV `actors.csv`.

        Utiliza un lock de hilo para evitar condiciones de carrera si se ejecuta en modo concurrente.

        Args:
            actor (Actor): Objeto Actor a guardar.
        """
        with actor_lock:
            with open(ACTORS_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    actor.id,
                    actor.name  
                ])
