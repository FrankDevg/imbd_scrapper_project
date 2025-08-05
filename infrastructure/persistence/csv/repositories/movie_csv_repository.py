import csv
import os
import threading
from typing import Optional
from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository

MOVIES_CSV = "data/movies.csv"
MOVIE_HEADERS = ["id", "imdb_id", "title", "year", "rating", "duration_minutes", "metascore"]
movie_lock = threading.Lock()

class MovieCsvRepository(MovieRepository):
    """
    Implementación del repositorio de películas que persiste datos en formato CSV.
    """
    def __init__(self):
        os.makedirs(os.path.dirname(MOVIES_CSV), exist_ok=True)
        if not os.path.exists(MOVIES_CSV):
            with open(MOVIES_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(MOVIE_HEADERS)

    def _get_next_id(self) -> int:
        """Lee el CSV para determinar el siguiente ID disponible."""
        with open(MOVIES_CSV, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) # Saltar encabezados
            last_id = 0
            for row in reader:
                if row:
                    last_id = int(row[0])
            return last_id + 1

    def save(self, movie: Movie) -> Movie:
        """
        Guarda una película en CSV, asignándole un nuevo ID si no lo tiene,
        y retorna el objeto Movie con el ID asignado.
        """
        with movie_lock:
            if movie.id is None:
                movie.id = self._get_next_id()
            
            with open(MOVIES_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    movie.id,
                    movie.imdb_id,
                    movie.title,
                    movie.year,
                    movie.rating,
                    movie.duration_minutes or "",
                    movie.metascore or ""
                ])
            return movie

    def find_by_imdb_id(self, imdb_id: str) -> Optional[Movie]:
        """
        Busca una película por su ID de IMDb en el archivo CSV.
        """
        with movie_lock:
            with open(MOVIES_CSV, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["imdb_id"] == imdb_id:
                        # Reconstruye el objeto Movie a partir de la fila del CSV
                        return Movie(
                            id=int(row["id"]),
                            imdb_id=row["imdb_id"],
                            title=row["title"],
                            year=int(row["year"]),
                            rating=float(row["rating"]),
                            duration_minutes=int(row["duration_minutes"]) if row["duration_minutes"] else None,
                            metascore=int(row["metascore"]) if row["metascore"] else None,
                            actors=[] # La lista de actores se carga por separado en el caso de uso
                        )
        return None