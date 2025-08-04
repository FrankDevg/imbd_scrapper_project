from domain.models.movie import Movie
from domain.models.actor import Actor
from domain.models.movie_actor import MovieActor

from domain.repositories.movie_repository import MovieRepository
from domain.repositories.actor_repository import ActorRepository
from domain.repositories.movie_actor_repository import MovieActorRepository

class SaveMovieWithActorsCsvUseCase:
    """
    Caso de uso que guarda una película y sus actores asociados en formato CSV,
    utilizando repositorios desacoplados que representan una relación N:M.
    """

    def __init__(
        self,
        movie_repository: MovieRepository,
        actor_repository: ActorRepository,
        movie_actor_repository: MovieActorRepository
    ):
        """
        Constructor del caso de uso para persistencia en CSV.

        Args:
            movie_repository (MovieRepository): Repositorio para guardar películas.
            actor_repository (ActorRepository): Repositorio para guardar actores.
            movie_actor_repository (MovieActorRepository): Repositorio para guardar relaciones película-actor.
        """
        self.movie_repo = movie_repository
        self.actor_repo = actor_repository
        self.movie_actor_repo = movie_actor_repository

    def execute(self, movie: Movie) -> None:
        """
        Ejecuta la validación y el guardado de una película y sus actores en CSV.

        Args:
            movie (Movie): Objeto que contiene los datos de la película y su reparto.
        """
        # Validaciones básicas de datos
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

        # Guardar película en CSV
        self.movie_repo.save(movie)

        # Guardar actores y relaciones N:M en CSV
        for actor in movie.actors:
            if isinstance(actor.name, str) and actor.name.strip():
                self.actor_repo.save(actor)
                self.movie_actor_repo.save(MovieActor(movie_id=movie.id, actor_id=actor.id))
