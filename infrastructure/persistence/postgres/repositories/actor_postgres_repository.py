from domain.models.actor import Actor
from domain.repositories.actor_repository import ActorRepository
from psycopg2 import DatabaseError

class ActorPostgresRepository(ActorRepository):
    """
    Implementación del repositorio de actores utilizando una base de datos PostgreSQL.

    Este repositorio emplea un procedimiento almacenado para insertar un actor solo si no existe,
    y luego recupera el ID correspondiente desde la tabla `actors`.
    """

    def __init__(self, conn):
        """
        Constructor del repositorio.

        Args:
            conn: Conexión activa a la base de datos PostgreSQL.
        """
        self.conn = conn

    def save(self, actor: Actor) -> int:
        """
        Guarda un actor en la base de datos PostgreSQL, asegurando que no se duplique.

        Utiliza un procedimiento almacenado `insert_actor_if_not_exists(name)` que debe estar
        previamente creado en la base de datos. Luego obtiene el ID correspondiente del actor.

        Args:
            actor (Actor): Objeto Actor a guardar.

        Returns:
            int: ID del actor guardado o existente en la base de datos.
                 Retorna None en caso de error o si no se encuentra el ID.
        """
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
