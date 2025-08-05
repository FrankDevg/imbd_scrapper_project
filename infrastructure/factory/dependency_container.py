
from domain.interfaces.use_case_interface import UseCaseInterface
from domain.interfaces.scraper_interface import ScraperInterface

from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase
from application.use_cases.composite_save_movie_with_actors_use_case import CompositeSaveMovieWithActorsUseCase
from infrastructure.persistence.csv.repositories.movie_csv_repository import MovieCsvRepository
from infrastructure.persistence.csv.repositories.actor_csv_repository import ActorCsvRepository
from infrastructure.persistence.csv.repositories.movie_actor_csv_repository import MovieActorCsvRepository
from infrastructure.persistence.postgres.repositories.movie_postgres_repository import MoviePostgresRepository
from infrastructure.persistence.postgres.repositories.actor_postgres_repository import ActorPostgresRepository
from infrastructure.persistence.postgres.repositories.movie_actor_postgres_repository import MovieActorPostgresRepository
from infrastructure.scraper.imdb_scraper import ImdbScraper
from infrastructure.persistence.postgres.postgres_connection import connection_pool 
from infrastructure.network.proxy_provider import ProxyProvider
from infrastructure.network.tor_rotator import TorRotator

class DependencyContainer:
    """
    Un contenedor centralizado para la inyección de dependencias.
    Gestiona la creación y el ciclo de vida de los servicios de la aplicación.
    """
    def __init__(self, config):
        self.config = config
        self._db_connection = None
        self.proxy_provider = ProxyProvider()
        self.tor_rotator = TorRotator()

    def get_db_connection(self):
        """Gestiona la conexión a la BD para que se cree una sola vez."""
        if self._db_connection is None and connection_pool:
            self._db_connection = connection_pool.getconn()
        return self._db_connection

    def close_db_connection(self):
        """Cierra la conexión y la devuelve al pool."""
        if self._db_connection and connection_pool:
            connection_pool.putconn(self._db_connection)
            self._db_connection = None
            print("Conexión a la base de datos cerrada y devuelta al pool.")

    def get_csv_use_case(self) -> UseCaseInterface:
        """Construye y devuelve el caso de uso para CSV."""
        return SaveMovieWithActorsCsvUseCase(
            movie_repository=MovieCsvRepository(),
            actor_repository=ActorCsvRepository(),
            movie_actor_repository=MovieActorCsvRepository()
        )

    def get_postgres_use_case(self) -> UseCaseInterface:
        """Construye y devuelve el caso de uso para PostgreSQL."""
        conn = self.get_db_connection()
        return SaveMovieWithActorsPostgresUseCase(
            movie_repository=MoviePostgresRepository(conn),
            actor_repository=ActorPostgresRepository(conn),
            movie_actor_repository=MovieActorPostgresRepository(conn)
        )

    def get_composite_use_case(self) -> UseCaseInterface:
        """Construye el caso de uso compuesto."""
        use_cases = [self.get_csv_use_case(), self.get_postgres_use_case()]
        return CompositeSaveMovieWithActorsUseCase(use_cases)

    def get_scraper(self) -> ScraperInterface:
        """Construye y devuelve el scraper principal."""
        use_case = self.get_composite_use_case()
        return ImdbScraper(
            use_case=use_case,
            proxy_provider=self.proxy_provider,
            tor_rotator=self.tor_rotator,
            engine=self.config.SCRAPER_ENGINE
        )