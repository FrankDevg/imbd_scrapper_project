from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository
from psycopg2 import DatabaseError

class MoviePostgresRepository(MovieRepository):
    """
    Implementación del repositorio de películas utilizando PostgreSQL como sistema de persistencia.

    Inserta una película solo si no existe previamente, usando un procedimiento almacenado,
    y luego recupera su ID para asociarla con otros datos.
    """

    def __init__(self, conn):
        """
        Constructor del repositorio.

        Args:
            conn: Objeto de conexión activa a la base de datos PostgreSQL.
        """
        self.conn = conn

    def save(self, movie: Movie) -> int:
        """
        Guarda una película en la base de datos PostgreSQL, evitando duplicados mediante
        un procedimiento almacenado `insert_movie_if_not_exists`.

        Luego consulta y devuelve el ID de la película insertada o existente.

        Args:
            movie (Movie): Objeto Movie a persistir.

        Returns:
            int: ID de la película en la base de datos, o None si ocurre un error.
        """
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
