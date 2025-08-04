from domain.interfaces.use_case_interface import UseCaseInterface

from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase
from application.use_cases.composite_save_movie_with_actors_use_case import CompositeSaveMovieWithActorsUseCase

from infrastructure.persistence.csv.repositories.movie_csv_repository import MovieCsvRepository
from infrastructure.persistence.csv.repositories.actor_csv_repository import ActorCsvRepository
from infrastructure.persistence.csv.repositories.movie_actor_csv_repository import MovieActorCsvRepository
from infrastructure.persistence.csv.init_csv_files import init_csv_files

from infrastructure.persistence.postgres.postgres_connection import get_postgres_connection
from infrastructure.persistence.postgres.repositories.movie_postgres_repository import MoviePostgresRepository
from infrastructure.persistence.postgres.repositories.actor_postgres_repository import ActorPostgresRepository
from infrastructure.persistence.postgres.repositories.movie_actor_postgres_repository import MovieActorPostgresRepository


def get_csv_use_case() -> UseCaseInterface:
    """
    Fábrica que construye el caso de uso de guardado usando repositorios CSV.

    Inicializa los archivos CSV necesarios y crea instancias de los repositorios
    correspondientes para películas, actores y relaciones N:M.

    Returns:
        SaveMovieWithActorsCsvUseCase: Caso de uso listo para guardar datos en CSV.
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


def get_save_movie_with_actors_postgres_use_case() -> UseCaseInterface:
    """
    Fábrica que construye el caso de uso de guardado usando repositorios PostgreSQL.

    Establece la conexión a la base de datos y crea los repositorios correspondientes
    para manejar la persistencia en PostgreSQL.

    Returns:
        SaveMovieWithActorsPostgresUseCase: Caso de uso listo para guardar datos en base de datos.
    """
    conn = get_postgres_connection()
    movie_repo = MoviePostgresRepository(conn)
    actor_repo = ActorPostgresRepository(conn)
    movie_actor_repo = MovieActorPostgresRepository(conn)

    return SaveMovieWithActorsPostgresUseCase(
        movie_repository=movie_repo,
        actor_repository=actor_repo,
        movie_actor_repository=movie_actor_repo
    )


def get_composite_use_case() -> UseCaseInterface:
    """
    Fábrica que construye el caso de uso compuesto, que guarda tanto en CSV como en PostgreSQL.

    Orquesta ambos casos de uso para realizar el guardado simultáneo en múltiples fuentes de persistencia.

    Returns:
        CompositeSaveMovieWithActorsUseCase: Caso de uso que combina CSV y PostgreSQL.
    """
    csv_use_case = get_csv_use_case()
    postgres_use_case = get_save_movie_with_actors_postgres_use_case()
    
    use_cases_list = [csv_use_case, postgres_use_case]
    
    return CompositeSaveMovieWithActorsUseCase(use_cases=use_cases_list)
