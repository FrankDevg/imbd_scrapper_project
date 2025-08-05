import logging
from typing import Optional
from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository
from psycopg2 import DatabaseError

logger = logging.getLogger(__name__)

class ActorPostgresRepository(ActorRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, actor: Actor) -> Actor: 
        """
        Guarda un actor usando un procedimiento almacenado y retorna el objeto completo.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM upsert_actor(%s);", (actor.name,))
                actor_data = cur.fetchone()
                self.conn.commit()
                return Actor(id=actor_data[0], name=actor_data[1])
        except DatabaseError as e:
            logger.error(f"Error al guardar actor '{actor.name}': {e}")
            self.conn.rollback()
            raise 

    def find_by_name(self, name: str) -> Optional[Actor]:
        """
        Busca un actor por su nombre en la base de datos.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, name FROM actors WHERE name = %s", (name,))
                actor_data = cur.fetchone()
                if actor_data:
                    return Actor(id=actor_data[0], name=actor_data[1])
                return None
        except DatabaseError as e:
            logger.error(f"Error al buscar actor por nombre '{name}': {e}")
            self.conn.rollback()
            return None