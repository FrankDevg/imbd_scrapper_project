from domain.models.movie import Movie
from application.use_cases.save_movie_with_actors_csv_use_case import SaveMovieWithActorsCsvUseCase
from application.use_cases.save_movie_with_actors_postgres_use_case import SaveMovieWithActorsPostgresUseCase

class CompositeSaveMovieWithActorsUseCase:
    """
    Caso de uso compuesto que encapsula la lógica de guardado de una película con sus actores
    en múltiples destinos de persistencia (CSV y PostgreSQL).

    Este patrón permite desacoplar el orquestador de las implementaciones concretas de almacenamiento,
    facilitando la extensión a nuevos repositorios si es necesario.
    """

    def __init__(
        self,
        csv_use_case: SaveMovieWithActorsCsvUseCase,
        postgres_use_case: SaveMovieWithActorsPostgresUseCase
    ):
        """
        Constructor del caso de uso compuesto.

        Args:
            csv_use_case (SaveMovieWithActorsCsvUseCase): Caso de uso encargado de guardar en CSV.
            postgres_use_case (SaveMovieWithActorsPostgresUseCase): Caso de uso encargado de guardar en PostgreSQL.
        """
        self.csv_use_case = csv_use_case
        self.postgres_use_case = postgres_use_case

    def execute(self, movie: Movie) -> None:
        """
        Ejecuta ambos casos de uso de guardado (CSV y PostgreSQL) en paralelo.

        Args:
            movie (Movie): Objeto Movie que contiene la información a persistir.
        """
        self.csv_use_case.execute(movie)
        self.postgres_use_case.execute(movie)
