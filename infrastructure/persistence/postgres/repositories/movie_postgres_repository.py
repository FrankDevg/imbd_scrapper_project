from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository
from psycopg2 import DatabaseError


class MoviePostgresRepository(MovieRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, movie: Movie) -> int:
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CALL insert_movie_if_not_exists(%s, %s, %s, %s, %s, %s);
                """, (
                    movie.imdb_id,
                    movie.title,
                    movie.year,
                    movie.rating,
                    movie.duration_minutes,
                    movie.metascore
                ))

                cur.execute("SELECT id FROM movies WHERE imdb_id = %s", (movie.imdb_id,))
                movie_id = cur.fetchone()

                self.conn.commit()
                return movie_id[0] if movie_id else None

        except DatabaseError as e:
            self.conn.rollback()
            return None
