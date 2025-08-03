# infrastructure/factory/use_case_factory.py

from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from infrastructure.persistence.csv.repositories.movie_csv_repository import MovieCsvRepository
from infrastructure.persistence.csv.repositories.actor_csv_repository import ActorCsvRepository
from infrastructure.persistence.csv.repositories.movie_actor_csv_repository import MovieActorCsvRepository

def get_csv_use_case() -> SaveMovieWithActorsCsvUseCase:
    """
    Fábrica que construye el caso de uso con repositorios basados en CSV.
    """
    movie_repo = MovieCsvRepository()
    actor_repo = ActorCsvRepository()
    movie_actor_repo = MovieActorCsvRepository()

    return SaveMovieWithActorsCsvUseCase(
        movie_repository=movie_repo,
        actor_repository=actor_repo,
        movie_actor_repository=movie_actor_repo
    )
