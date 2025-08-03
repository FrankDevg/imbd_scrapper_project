# infrastructure/persistence/db_handler.py

import psycopg2
from domain.models import Movie, Actor
from typing import List

def save_to_postgres(movies: List[Movie], db_config: dict):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM actores")
    cursor.execute("DELETE FROM peliculas")
    connection.commit()

    for movie in movies:
        cursor.execute("""
            INSERT INTO peliculas (id, titulo, anio, calificacion, duracion, metascore)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            movie.id, movie.title, movie.year, movie.rating,
            movie.duration_minutes, movie.metascore
        ))

        for actor in movie.actors:
            cursor.execute("""
                INSERT INTO actores (id, pelicula_id, nombre)
                VALUES (%s, %s, %s)
            """, (actor.id, actor.movie_id, actor.name))

    connection.commit()
    cursor.close()
    connection.close()
