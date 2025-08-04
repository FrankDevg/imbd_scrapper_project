from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository
from psycopg2 import DatabaseError


class ActorPostgresRepository(ActorRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, actor: Actor) -> int:
        try:
            with self.conn.cursor() as cur:
                # Llama al procedimiento para insertar solo si no existe
                cur.execute("""
                    CALL insert_actor_if_not_exists(%s);
                """, (actor.name,))

                # Luego busca el ID insertado o existente
                cur.execute("SELECT id FROM actors WHERE name = %s", (actor.name,))
                actor_id = cur.fetchone()

                self.conn.commit()
                return actor_id[0] if actor_id else None

        except DatabaseError as e:
            self.conn.rollback()
            return None
