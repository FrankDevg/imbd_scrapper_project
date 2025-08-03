from infrastructure.persistence.postgres.postgres_connection import get_postgres_connection
from infrastructure.persistence.postgres.repositories.movie_postgres_repository import MoviePostgresRepository

def get_movie_postgres_repository():
    conn = get_postgres_connection()
    return MoviePostgresRepository(conn)
