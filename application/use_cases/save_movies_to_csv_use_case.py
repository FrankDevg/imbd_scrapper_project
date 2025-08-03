# application/use_cases/save_movies_use_case.py

from domain.models import Movie
from infrastructure.persistence.csv_writer import append_movie, append_actors

class SaveMoviesToCsvUseCase:
    def execute(self, movie: Movie) -> None:
        if not isinstance(movie.title, str) or movie.title.strip() in ["", "N/A"]:
            return
        if not isinstance(movie.year, int) or not (1900 <= movie.year <= 2026):
            return
        if movie.rating is not None and not (0.0 <= movie.rating <= 10.0):
            movie.rating = None
        if movie.duration_minutes is not None and movie.duration_minutes <= 0:
            movie.duration_minutes = None
        if movie.metascore is not None and not (0 <= movie.metascore <= 100):
            movie.metascore = None
        
        movie.actors = [a for a in movie.actors if isinstance(a.name, str) and a.name.strip()]
        
        append_movie(movie)
        append_actors(movie.actors)
