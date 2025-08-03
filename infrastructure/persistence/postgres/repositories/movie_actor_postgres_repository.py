from domain.models.movie_actor import MovieActor
from domain.repositories.movie_actor_repository import MovieActorRepository

class MovieActorPostgresRepository(MovieActorRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, movie_actor: MovieActor) -> None:
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO movie_actor (movie_id, actor_id)
                VALUES (%s, %s)
                ON CONFLICT (movie_id, actor_id) DO NOTHING;
            """, (movie_actor.movie_id, movie_actor.actor_id))
            self.conn.commit()
