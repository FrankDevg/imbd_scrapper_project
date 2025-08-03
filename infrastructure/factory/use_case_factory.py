# infrastructure/factory/use_case_factory.py

from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase
from application.use_cases.composite_save_movie_with_actors_use_case import CompositeSaveMovieWithActorsUseCase
from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase

from infrastructure.persistence.csv.repositories.movie_csv_repository import MovieCsvRepository
from infrastructure.persistence.csv.repositories.actor_csv_repository import ActorCsvRepository
from infrastructure.persistence.csv.repositories.movie_actor_csv_repository import MovieActorCsvRepository
from infrastructure.persistence.csv.init_csv_files import init_csv_files
from infrastructure.persistence.postgres.postgres_connection import get_postgres_connection
from infrastructure.persistence.postgres.repositories.movie_postgres_repository import MoviePostgresRepository
from infrastructure.persistence.postgres.repositories.actor_postgres_repository import ActorPostgresRepository
from infrastructure.persistence.postgres.repositories.movie_actor_postgres_repository import MovieActorPostgresRepository

def get_csv_use_case() -> SaveMovieWithActorsCsvUseCase:
    """
    Fábrica que construye el caso de uso con repositorios basados en CSV.
    """
    init_csv_files()
    movie_repo = MovieCsvRepository()
    actor_repo = ActorCsvRepository()
    movie_actor_repo = MovieActorCsvRepository()

    return SaveMovieWithActorsCsvUseCase(
        movie_repository=movie_repo,
        actor_repository=actor_repo,
        movie_actor_repository=movie_actor_repo
    )
def get_save_movie_with_actors_postgres_use_case() -> SaveMovieWithActorsPostgresUseCase:
    conn = get_postgres_connection()
    movie_repo = MoviePostgresRepository(conn)
    actor_repo = ActorPostgresRepository(conn)
    movie_actor_repo = MovieActorPostgresRepository(conn)

    return SaveMovieWithActorsPostgresUseCase(
        movie_repository=movie_repo,
        actor_repository=actor_repo,
        movie_actor_repository=movie_actor_repo
    )
def get_composite_use_case() -> CompositeSaveMovieWithActorsUseCase:
    csv_use_case = get_csv_use_case()
    postgres_use_case = get_save_movie_with_actors_postgres_use_case()
    return CompositeSaveMovieWithActorsUseCase(csv_use_case, postgres_use_case)