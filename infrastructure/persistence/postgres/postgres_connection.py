import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from shared.config import config
import logging

logger = logging.getLogger(__name__)

connection_pool = None
try:
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
    logger.info("Pool de conexiones a PostgreSQL creado.")
except psycopg2.OperationalError as e:
    logger.error(f"Error al crear el pool de conexiones: {e}")

@contextmanager
def get_connection():
    if not connection_pool:
        raise ConnectionError("El pool de conexiones no está disponible.")
    
    conn = None
    try:
        conn = connection_pool.getconn()
        yield conn
    finally:
        if conn:
            connection_pool.putconn(conn)