-- =============================================
--  Archivo: load_from_csv.sql
--  Propósito: Cargar datos desde archivos CSV a las tablas del proyecto IMDb
--  Autor: Andrés Ruiz
--  Fecha de creación: 2025-08-03
--  Nota: Requiere permisos en el servidor y acceso a las rutas locales especificadas.
--        Asegúrate de reemplazar '/PATH_CAMBIAR/to/*.csv' con la ruta absoluta correcta.
-- =============================================

-- =============================================
-- CARGAR PELÍCULAS
-- Carga los datos de películas desde un archivo CSV con cabecera.
-- =============================================
COPY movies(id, title, year, rating, duration_minutes, metascore)
FROM '/PATH_CAMBIAR/to/movies.csv' 
DELIMITER ',' 
CSV HEADER;

-- =============================================
-- CARGAR ACTORES
-- Carga los datos de actores desde un archivo CSV con cabecera.
-- =============================================
COPY actors(id, name)
FROM '/PATH_CAMBIAR/to/actors.csv' 
DELIMITER ',' 
CSV HEADER;

-- =============================================
-- CARGAR RELACIONES PELÍCULA–ACTOR
-- Carga relaciones N:M entre películas y actores desde archivo CSV.
-- =============================================
COPY movie_actor(movie_id, actor_id)
FROM '/PATH_CAMBIAR/to/movie_actor.csv' 
DELIMITER ',' 
CSV HEADER;
