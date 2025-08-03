# application/use_cases/composite_save_movie_with_actors_use_case.py

from domain.models.movie import Movie
from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase

class CompositeSaveMovieWithActorsUseCase:
    def __init__(
        self,
        csv_use_case: SaveMovieWithActorsCsvUseCase,
        postgres_use_case: SaveMovieWithActorsPostgresUseCase
    ):
        self.csv_use_case = csv_use_case
        self.postgres_use_case = postgres_use_case

    def execute(self, movie: Movie) -> None:
        self.csv_use_case.execute(movie)
        self.postgres_use_case.execute(movie)
