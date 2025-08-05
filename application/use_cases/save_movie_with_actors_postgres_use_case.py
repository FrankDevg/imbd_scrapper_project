

import logging
from domain.models.movie import Movie
from domain.models.actor import Actor
from domain.models.movie_actor import MovieActor
from domain.interfaces.use_case_interface import UseCaseInterface
from domain.repositories.movie_repository import MovieRepository
from domain.repositories.actor_repository import ActorRepository
from domain.repositories.movie_actor_repository import MovieActorRepository

logger = logging.getLogger(__name__)


class SaveMovieWithActorsPostgresUseCase(UseCaseInterface):
    """
    Caso de uso para guardar una película y sus actores en PostgreSQL,
    manejando duplicados y orquestando los repositorios.
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
        Ejecuta el manejo de duplicados y guardado.
        Confía en que el objeto 'movie' ya es válido.
        """
        try:
            

            # Manejo de duplicados de películas
            existing_movie = self.movie_repo.find_by_imdb_id(movie.imdb_id)
            if existing_movie:
                logger.info(f"La película '{movie.title}' ya existe en la BD. Saltando.")
                return

            # Uso correcto del valor de retorno
            saved_movie = self.movie_repo.save(movie)
            if not saved_movie or not saved_movie.id:
                logger.error(f"Error al guardar la película '{movie.title}' o al obtener su ID.")
                return

            relations_to_save = []
            for actor in movie.actors:
                # Manejo de duplicados de actores
                existing_actor = self.actor_repo.find_by_name(actor.name)
                if existing_actor:
                    saved_actor = existing_actor
                else:
                    saved_actor = self.actor_repo.save(actor)
                
                if saved_actor and saved_actor.id:
                    relations_to_save.append(
                        MovieActor(movie_id=saved_movie.id, actor_id=saved_actor.id)
                    )

            if relations_to_save:
                self.movie_actor_repo.save_many(relations_to_save)
                logger.info(f"Guardada película '{saved_movie.title}' con {len(relations_to_save)} actores.")

        except Exception as e: 
            logger.error(f"Error en la base de datos al procesar '{movie.title}': {e}")