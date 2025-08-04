-- =============================================
--  Archivo: procedures.sql
--  Propósito: Procedimientos para inserción segura desde el scraper
--  Autor: Andrés Ruiz
--  Fecha: 2025-08-03
--  Uso: Llamados desde Python para insertar datos solo si no existen
-- =============================================


-- =============================================
-- PROCEDURE: insert_movie_if_not_exists
-- Descripción: Inserta una película solo si no existe ya en la tabla `movies`
-- Identificación se realiza por imdb_id
-- =============================================
CREATE OR REPLACE PROCEDURE insert_movie_if_not_exists(
    p_imdb_id TEXT,
    p_title TEXT,
    p_year INT,
    p_rating FLOAT,
    p_duration INT,
    p_metascore INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM movies WHERE imdb_id = p_imdb_id
    ) THEN
        INSERT INTO movies (imdb_id, title, year, rating, duration_minutes, metascore)
        VALUES (p_imdb_id, p_title, p_year, p_rating, p_duration, p_metascore);
    END IF;
END;
$$;


-- =============================================
-- PROCEDURE: insert_actor_if_not_exists
-- Descripción: Inserta un actor si no existe ya en la tabla `actors`
-- Identificación se realiza por nombre único
-- =============================================
CREATE OR REPLACE PROCEDURE insert_actor_if_not_exists(
    p_name TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM actors WHERE name = p_name
    ) THEN
        INSERT INTO actors (name)
        VALUES (p_name);
    END IF;
END;
$$;


-- =============================================
-- PROCEDURE: insert_movie_actor_if_not_exists
-- Descripción: Inserta una relación entre película y actor (N:M)
-- Solo si no existe ya en la tabla `movie_actor`
-- =============================================
CREATE OR REPLACE PROCEDURE insert_movie_actor_if_not_exists(
    p_movie_id INT,
    p_actor_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM movie_actor WHERE movie_id = p_movie_id AND actor_id = p_actor_id
    ) THEN
        INSERT INTO movie_actor (movie_id, actor_id)
        VALUES (p_movie_id, p_actor_id);
    END IF;
END;
$$;
