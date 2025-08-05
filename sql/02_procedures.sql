-- =============================================
--  Archivo: functions.sql
--  Propósito: Funciones para la inserción y consulta segura de datos.
--  Autor: Andrés Ruiz
--  Fecha: 2025-08-04
--  Estrategia: Se utilizan FUNCIONES con INSERT ... ON CONFLICT y RETURNING
--               para realizar operaciones "upsert" atómicas y eficientes,
--               reduciendo las llamadas a la base de datos desde la aplicación.
-- =============================================


-- =============================================
--  FUNCTION: upsert_movie
--  Descripción: Inserta o ignora una película basada en su imdb_id (clave única)
--               y siempre devuelve la fila completa (ya sea la nueva o la existente).
-- =============================================
CREATE OR REPLACE FUNCTION upsert_movie(
    p_imdb_id TEXT,
    p_title TEXT,
    p_year INT,
    p_rating FLOAT,
    p_duration INT,
    p_metascore INT
)
RETURNS SETOF movies AS
$$
BEGIN
    RETURN QUERY
    WITH inserted AS (
        INSERT INTO movies (imdb_id, title, year, rating, duration_minutes, metascore)
        VALUES (p_imdb_id, p_title, p_year, p_rating, p_duration, p_metascore)
        ON CONFLICT (imdb_id) DO NOTHING
        RETURNING *
    )
    SELECT * FROM inserted
    UNION ALL
    SELECT * FROM movies WHERE imdb_id = p_imdb_id AND NOT EXISTS (SELECT 1 FROM inserted);
END;
$$ LANGUAGE plpgsql;


-- =============================================
--  FUNCTION: upsert_actor
--  Descripción: Inserta un actor si no existe (basado en el nombre como clave única)
--               y siempre devuelve la fila completa del actor.
-- =============================================
CREATE OR REPLACE FUNCTION upsert_actor(
    p_name TEXT
)
RETURNS SETOF actors AS
$$
BEGIN
    RETURN QUERY
    WITH inserted AS (
        INSERT INTO actors (name)
        VALUES (p_name)
        ON CONFLICT (name) DO NOTHING
        RETURNING *
    )
    SELECT * FROM inserted
    UNION ALL
    SELECT * FROM actors WHERE name = p_name AND NOT EXISTS (SELECT 1 FROM inserted);
END;
$$ LANGUAGE plpgsql;


-- =============================================
--  FUNCTION: upsert_movie_actor
--  Descripción: Inserta una relación película-actor si no existe.
--               No devuelve nada porque la tabla de relación no tiene datos adicionales.
-- =============================================
CREATE OR REPLACE FUNCTION upsert_movie_actor(
    p_movie_id INT,
    p_actor_id INT
)
RETURNS void AS 
$$
BEGIN
    INSERT INTO movie_actor (movie_id, actor_id)
    VALUES (p_movie_id, p_actor_id)
    ON CONFLICT (movie_id, actor_id) DO NOTHING; 
END;
$$ LANGUAGE plpgsql;