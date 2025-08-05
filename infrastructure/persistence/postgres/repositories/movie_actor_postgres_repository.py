import logging
from typing import List
from domain.models.movie_actor import MovieActor
from domain.repositories.movie_actor_repository import MovieActorRepository
from psycopg2 import DatabaseError
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

class MovieActorPostgresRepository(MovieActorRepository):
    """
    Implementación del repositorio para manejar relaciones N:M en PostgreSQL.
    """
    def __init__(self, conn):
        self.conn = conn

    def save(self, relation: MovieActor) -> None:
        """
        Guarda una única relación película-actor en PostgreSQL.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * from upsert_movie_actor(%s, %s);", 
                            (relation.movie_id, relation.actor_id))
                self.conn.commit()
        except DatabaseError as e:
            logger.error(f"Error al guardar relación movie_id={relation.movie_id}, actor_id={relation.actor_id}: {e}")
            self.conn.rollback()
            raise

    def save_many(self, relations: List[MovieActor]) -> None:
        """
        Guarda una lista de relaciones película-actor de forma eficiente.
        """
        if not relations:
            return
        
        try:
            with self.conn.cursor() as cur:
                values = [(r.movie_id, r.actor_id) for r in relations]
                
                for value in values:
                     cur.execute("SELECT * from upsert_movie_actor(%s, %s);", value)

                self.conn.commit()
        except DatabaseError as e:
            logger.error(f"Error al guardar múltiples relaciones: {e}")
            self.conn.rollback()
            raise