from domain.models.movie_actor import MovieActor
from domain.repositories.movie_actor_repository import MovieActorRepository
from psycopg2 import DatabaseError

class MovieActorPostgresRepository(MovieActorRepository):
    """
    Implementación del repositorio para manejar relaciones N:M entre películas y actores
    utilizando una base de datos PostgreSQL.

    Utiliza un procedimiento almacenado para insertar la relación si no existe previamente.
    """

    def __init__(self, conn):
        """
        Constructor del repositorio.

        Args:
            conn: Conexión activa a la base de datos PostgreSQL.
        """
        self.conn = conn

    def save(self, movie_actor: MovieActor) -> None:
        """
        Guarda una relación entre una película y un actor en PostgreSQL,
        evitando duplicados mediante un procedimiento almacenado.

        Args:
            movie_actor (MovieActor): Objeto que representa la relación a guardar.
        """
        try:
            with self.conn.cursor() as cur:
                # Llamar al procedimiento almacenado para insertar solo si no existe
                cur.execute("""
                    CALL insert_movie_actor_if_not_exists(%s, %s);
                """, (
                    movie_actor.movie_id,
                    movie_actor.actor_id
                ))
                self.conn.commit()
        except DatabaseError as e:
            self.conn.rollback()
