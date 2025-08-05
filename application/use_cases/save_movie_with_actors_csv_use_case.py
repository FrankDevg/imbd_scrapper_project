import logging
from domain.models.movie import Movie
from domain.models.actor import Actor
from domain.models.movie_actor import MovieActor
from domain.interfaces.use_case_interface import UseCaseInterface
from domain.repositories.movie_repository import MovieRepository
from domain.repositories.actor_repository import ActorRepository
from domain.repositories.movie_actor_repository import MovieActorRepository

logger = logging.getLogger(__name__)

class SaveMovieWithActorsCsvUseCase(UseCaseInterface):
    """
    Caso de uso que guarda una película y sus actores en formato CSV.
    Orquesta los repositorios y confía en que los modelos de dominio ya son válidos.
    """

    def __init__(
        self,
        movie_repository: MovieRepository,
        actor_repository: ActorRepository,
        movie_actor_repository: MovieActorRepository
    ):
        self.movie_repo = movie_repository
        self.actor_repo = actor_repository
        self.movie_actor_repo = movie_actor_repository

    def execute(self, movie: Movie) -> None:
        """
        Ejecuta el guardado de una película y sus actores en CSV, manejando duplicados.
        """
        try:
            # Manejo de duplicados: comprueba si la película ya existe por su ID de IMDb.
            # Nota: para CSV, find_by_imdb_id puede ser una operación costosa si el archivo es grande.
            # Se asume una implementación optimizada o se acepta el costo.
            existing_movie = self.movie_repo.find_by_imdb_id(movie.imdb_id)
            if existing_movie:
                logger.info(f"La película '{movie.title}' ya existe en el CSV. Saltando.")
                return

            # Guarda la película. En CSV, el 'id' puede no generarse automáticamente,
            # por lo que asumimos que el modelo Movie ya tiene un ID o se maneja internamente.
            saved_movie = self.movie_repo.save(movie)

            relations_to_save = []
            for actor in movie.actors:
                # Manejo de duplicados de actores.
                existing_actor = self.actor_repo.find_by_name(actor.name)
                if existing_actor:
                    saved_actor = existing_actor
                else:
                    saved_actor = self.actor_repo.save(actor)
                
                # Asegurarse de que ambos IDs existen antes de crear la relación.
                if saved_movie.id and saved_actor.id:
                    relations_to_save.append(
                        MovieActor(movie_id=saved_movie.id, actor_id=saved_actor.id)
                    )

            if relations_to_save:
                self.movie_actor_repo.save_many(relations_to_save)
                logger.info(f"Guardada película '{saved_movie.title}' en CSV con {len(relations_to_save)} actores.")

        except Exception as e:
            logger.error(f"Error al escribir en CSV para la película '{movie.title}': {e}")