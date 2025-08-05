# En: infrastructure/persistence/postgres/postgres_connection.py

import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from shared.config import config
import logging

logger = logging.getLogger(__name__)

# Pool de conexiones para manejar múltiples conexiones a la base de datos PostgreSQL
try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=config.POSTGRES_MAX_CONNECTIONS,  
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
    logger.info("Pool de conexiones a PostgreSQL creado exitosamente.")
except psycopg2.OperationalError as e:
    logger.error(f"Error al crear el pool de conexiones a PostgreSQL: {e}")
    connection_pool = None

# --- Se crea un "gestor de contexto" para usar el pool de forma segura ---
@contextmanager
def get_connection():
    """
    Obtiene una conexión del pool y se asegura de devolverla
    incluso si ocurren errores.
    """
    if connection_pool is None:
        raise ConnectionError("El pool de conexiones no está disponible.")
    
    connection = None
    try:
        # Pide una conexión al pool
        connection = connection_pool.getconn()
        yield connection
    finally:
        # Devuelve la conexión al pool cuando el bloque 'with' termina
        if connection:
            connection_pool.putconn(connection)
# infrastructure/persistence/postgres/postgres_connection.py



# --- Gestor de contexto que ahora retorna un cursor ---
@contextmanager
def get_cursor():
    """
    Obtiene una conexión del pool, crea un cursor, y se asegura de
    cerrar el cursor y devolver la conexión al pool.
    """
    if connection_pool is None:
        raise ConnectionError("El pool de conexiones no está disponible.")
    
    conn = None
    cur = None
    try:
        conn = connection_pool.getconn()
        cur = conn.cursor()
        yield cur
    except Exception as e:
        # En caso de error, hacemos rollback
        if conn:
            conn.rollback()
        raise
    finally:
        # Cerrar el cursor y devolver la conexión al pool
        if cur:
            cur.close()
        if conn:
            conn.commit()  
            connection_pool.putconn(conn)