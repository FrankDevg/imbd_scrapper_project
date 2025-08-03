import csv
import os
import threading
from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository

MOVIES_CSV = "data/movies.csv"
MOVIE_HEADERS = ["id", "imbd_id", "title", "year", "rating", "duration_minutes", "metascore","actors"]
movie_lock = threading.Lock()

class MovieCsvRepository(MovieRepository):
    def __init__(self):
        os.makedirs(os.path.dirname(MOVIES_CSV), exist_ok=True)
        if not os.path.exists(MOVIES_CSV):
            with open(MOVIES_CSV, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(MOVIE_HEADERS)

    def save(self, movie: Movie) -> None:
        with movie_lock:
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
