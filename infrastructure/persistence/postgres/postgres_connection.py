# infrastructure/persistence/postgres/postgres_connection.py

import psycopg2
from shared.config import config

def get_postgres_connection():
 
    return psycopg2.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
