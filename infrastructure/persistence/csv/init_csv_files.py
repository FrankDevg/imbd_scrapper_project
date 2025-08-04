import os
import csv

# Rutas a los archivos de salida
OUTPUT_DIR = "data"
MOVIES_CSV = os.path.join(OUTPUT_DIR, "movies.csv")
ACTORS_CSV = os.path.join(OUTPUT_DIR, "actors.csv")
MOVIE_ACTOR_CSV = os.path.join(OUTPUT_DIR, "movie_actor.csv")

def init_csv_files():
    """
    Inicializa los archivos CSV necesarios para almacenar datos de películas, actores y sus relaciones.

    Crea el directorio de salida si no existe, y escribe los encabezados correspondientes
    en cada archivo, sobrescribiendo cualquier contenido previo (modo "w").

    Archivos generados:
        - movies.csv: Contiene información detallada de las películas.
        - actors.csv: Contiene los nombres de los actores.
        - movie_actor.csv: Contiene las relaciones N:M entre películas y actores.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(MOVIES_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            "id", "imdb_id", "title", "year", "rating",
            "duration_minutes", "metascore", "actors"
        ])

    with open(ACTORS_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["id", "name"])

    with open(MOVIE_ACTOR_CSV, mode="w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["movie_id", "actor_id"])
