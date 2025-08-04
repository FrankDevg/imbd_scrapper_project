from domain.models.movie_actor import MovieActor
from domain.repositories.movie_actor_repository import MovieActorRepository
from psycopg2 import DatabaseError


class MovieActorPostgresRepository(MovieActorRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, movie_actor: MovieActor) -> None:
        try:
            with self.conn.cursor() as cur:
                # Llamar al procedimiento almacenado
                cur.execute("""
                    CALL insert_movie_actor_if_not_exists(%s, %s);
                """, (
                    movie_actor.movie_id,
                    movie_actor.actor_id
                ))
                self.conn.commit()
        except DatabaseError as e:
            self.conn.rollback()
