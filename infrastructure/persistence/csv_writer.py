import csv
import os
import threading
from typing import List
from domain.models import Movie, Actor

# Rutas de salida
OUTPUT_DIR = "data"
MOVIES_CSV = os.path.join(OUTPUT_DIR, "output_movies.csv")
ACTORS_CSV = os.path.join(OUTPUT_DIR, "output_actors.csv")

# Cabeceras explícitas (puedes cambiarlas si algún cliente pide nombres más legibles)
MOVIE_HEADERS = ["id", "title", "year", "rating", "duration_minutes", "metascore"]
ACTOR_HEADERS = ["id", "movie_id", "name"]

# Locks para escritura segura en entorno multihilo
movie_lock = threading.Lock()
actor_lock = threading.Lock()

def init_csv_files() -> None:
    """
    Inicializa los archivos CSV escribiendo solo los encabezados.
    Se llama una vez al inicio.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(MOVIES_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(MOVIE_HEADERS)

    with open(ACTORS_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(ACTOR_HEADERS)

def append_movie(movie: Movie) -> None:
    """
    Agrega una fila de película al archivo CSV de forma segura entre hilos.
    """
    with movie_lock:
        with open(MOVIES_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                movie.id,
                movie.title or "",
                movie.year or "",
                movie.rating or "",
                movie.duration_minutes if movie.duration_minutes is not None else "",
                movie.metascore if movie.metascore is not None else ""
            ])

def append_actors(actors: List[Actor]) -> None:
    """
    Agrega actores de una película al CSV correspondiente de forma segura.
    """
    if not actors:
        return

    with actor_lock:
        with open(ACTORS_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for actor in actors:
                writer.writerow([
                    actor.id,
                    actor.movie_id,
                    actor.name or ""
                ])
