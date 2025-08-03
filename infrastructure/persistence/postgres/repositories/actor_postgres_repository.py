from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository

class ActorPostgresRepository(ActorRepository):
    def __init__(self, conn):
        self.conn = conn

    def save(self, actor: Actor) -> int:
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actors (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id;
            """, (actor.name,))
            
            actor_id = cur.fetchone()
            if not actor_id:
                cur.execute("SELECT id FROM actors WHERE name = %s", (actor.name,))
                actor_id = cur.fetchone()

            self.conn.commit()
            return actor_id[0]
