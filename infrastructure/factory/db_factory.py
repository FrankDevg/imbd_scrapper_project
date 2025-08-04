from infrastructure.persistence.postgres.postgres_connection import get_postgres_connection
from infrastructure.persistence.postgres.repositories.movie_postgres_repository import MoviePostgresRepository

def get_movie_postgres_repository():
    """
    Fábrica que instancia y retorna un repositorio de películas para PostgreSQL.

    Establece una conexión con la base de datos y construye una instancia de MoviePostgresRepository.

    Returns:
        MoviePostgresRepository: Repositorio listo para interactuar con la base de datos PostgreSQL.
    """
    conn = get_postgres_connection()
    return MoviePostgresRepository(conn)
