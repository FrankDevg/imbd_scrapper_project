import re
from domain.models.movie import Movie
from domain.models.movie_actor import MovieActor
from domain.repositories.movie_repository import MovieRepository
from domain.repositories.actor_repository import ActorRepository
from domain.repositories.movie_actor_repository import MovieActorRepository

class SaveMovieWithActorsPostgresUseCase:
    """
    Caso de uso para guardar una película y sus actores relacionados en PostgreSQL.
    Realiza validaciones previas antes de persistir.
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
        Ejecuta el guardado de la película y los actores asociados, si los datos son válidos.
        """
        # 
        movie.imdb_id = movie.imdb_id.strip()
        if not isinstance(movie.imdb_id, str) or not re.match(r"^tt\d{7,}$", movie.imdb_id):
            return  

        movie.title = movie.title.strip()
        if not movie.title or len(movie.title) <= 1:
            return  

        if movie.year is not None and not (1888 <= movie.year <= 2100):
            return  

        if movie.rating is not None and not (0 <= movie.rating <= 10):
            return  
        if movie.duration_minutes is not None and not (1 <= movie.duration_minutes <= 600):
            return  

        if movie.metascore is not None and not (0 <= movie.metascore <= 100):
            return  

       
        try:
            movie_id = self.movie_repo.save(movie)
        except Exception:
            return  

        
        for actor in movie.actors:
            actor.name = actor.name.strip()
            if not actor.name or len(actor.name) <= 1:
                continue  
            try:
                actor_id = self.actor_repo.save(actor)
                self.movie_actor_repo.save(MovieActor(movie_id=movie_id, actor_id=actor_id))
            except Exception:
                continue  
