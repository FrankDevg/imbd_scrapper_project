from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository

class MoviePostgresRepository(MovieRepository):
    def __init__(self, conn):
        self.conn = conn

from psycopg2 import DatabaseError

class MoviePostgresRepository(MovieRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, movie: Movie) -> int:
        try:
            with self.conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO movies (imdb_id, title, year, rating, duration_minutes, metascore)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (imdb_id) DO NOTHING
                    RETURNING id;
                """, (
                    movie.imdb_id,
                    movie.title,
                    movie.year,
                    movie.rating,
                    movie.duration_minutes,
                    movie.metascore
                ))

                movie_id = cur.fetchone()
                if not movie_id:
                    cur.execute("SELECT id FROM movies WHERE imdb_id = %s", (movie.imdb_id,))
                    movie_id = cur.fetchone()

                self.conn.commit()
                return movie_id[0] if movie_id else None

        except DatabaseError as e:
            self.conn.rollback()  # 🧠 MUY IMPORTANTE
            return None
