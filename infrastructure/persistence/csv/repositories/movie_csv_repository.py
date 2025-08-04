import csv
import os
import threading
from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository

# Ruta del archivo CSV donde se guardan las películas
MOVIES_CSV = "data/movies.csv"

# Encabezados del archivo CSV
MOVIE_HEADERS = ["id", "imdb_id", "title", "year", "rating", "duration_minutes", "metascore", "actors"]

# Lock para evitar condiciones de carrera en entornos concurrentes
movie_lock = threading.Lock()

class MovieCsvRepository(MovieRepository):
    """
    Implementación del repositorio de películas que persiste datos en formato CSV.
    """

    def __init__(self):
        """
        Inicializa el repositorio, creando el archivo CSV con encabezados si no existe.
        """
        # Crea la carpeta 'data/' si no existe
        os.makedirs(os.path.dirname(MOVIES_CSV), exist_ok=True)

        # Crea el archivo con encabezados si aún no existe
        if not os.path.exists(MOVIES_CSV):
            with open(MOVIES_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(MOVIE_HEADERS)

    def save(self, movie: Movie) -> None:
        """
        Guarda una película en el archivo CSV. Los actores se almacenan como string separado por comas.
        """
        with movie_lock:  # Garantiza que un solo hilo escriba a la vez
            with open(MOVIES_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    movie.id,
                    movie.imdb_id,
                    movie.title,
                    movie.year,
                    movie.rating,
                    movie.duration_minutes or "",
                    movie.metascore or "",
                    ",".join(actor.name for actor in movie.actors)
                ])
