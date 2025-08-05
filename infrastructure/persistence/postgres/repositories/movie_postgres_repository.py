import logging
from typing import Optional
from domain.models.movie import Movie
from domain.repositories.movie_repository import MovieRepository
from psycopg2 import DatabaseError
from infrastructure.persistence.postgres.postgres_connection import get_cursor

logger = logging.getLogger(__name__)

class MoviePostgresRepository(MovieRepository):
    """
    Implementación del repositorio de películas utilizando PostgreSQL.
    """
    def __init__(self, conn):
        self.conn = conn

    def save(self, movie: Movie) -> Movie:
        """
        Guarda una película usando un procedimiento almacenado y retorna el objeto completo.
        """
        try:
            with get_cursor() as cur:
                cur.execute("SELECT * FROM upsert_movie(%s, %s, %s, %s, %s, %s);", (
                    movie.imdb_id, movie.title, movie.year, movie.rating,
                    movie.duration_minutes, movie.metascore
                ))
                movie_data = cur.fetchone() 
                return Movie(
                                id=movie_data[0],
                                imdb_id=movie_data[1],
                                title=movie_data[2],
                                year=movie_data[3],
                                rating=float(movie_data[4]),  
                                duration_minutes=movie_data[5], 
                                metascore=movie_data[6],
                                actors=[]  
                            )
                             
        except DatabaseError as e:
            logger.error(f"Error al guardar película '{movie.title}': {e}")
            self.conn.rollback()
            raise 

    def find_by_imdb_id(self, imdb_id: str) -> Optional[Movie]:
        """
        Busca una película por su ID de IMDb en la base de datos.
        """
        try:
            with get_cursor() as cur:
                cur.execute("""
                    SELECT id, imdb_id, title, year, rating, duration_minutes, metascore 
                    FROM movies WHERE imdb_id = %s
                """, (imdb_id,))
                
                movie_data = cur.fetchone()
                if movie_data:
                    return Movie(
                        id=movie_data[0], imdb_id=movie_data[1], title=movie_data[2],
                        year=movie_data[3], rating=float(movie_data[4]), 
                        duration_minutes=movie_data[5], metascore=movie_data[6],
                        actors=[] 
                    )
                return None
        except DatabaseError as e:
            logger.error(f"Error al buscar película por imdb_id '{imdb_id}': {e}")
            self.conn.rollback()
            return None