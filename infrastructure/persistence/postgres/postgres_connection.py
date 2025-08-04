
import psycopg2
from shared.config import config

def get_postgres_connection():
    """
    Establece y retorna una conexión a la base de datos PostgreSQL utilizando los parámetros
    definidos en el archivo de configuración compartido.

    La conexión se realiza usando psycopg2 y extrae los valores desde `shared.config.config`.

    Returns:
        connection (psycopg2.extensions.connection): Conexión activa a la base de datos.
    """
    return psycopg2.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
