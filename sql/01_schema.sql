-- =============================================
--  Archivo: schema.sql
--  Propósito: Definir la estructura base de datos para el proyecto IMDb Scraper
--  Autor: Andrés Ruiz
--  Fecha de creación: 2025-08-03
--  Descripción: Tablas relacionales para películas, actores y su relación N:M
-- =============================================

-- Elimina las tablas si ya existen para permitir recrear el esquema limpio
DROP TABLE IF EXISTS movie_actor;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS movies;

-- =============================================
-- Tabla: movies
-- Descripción: Contiene datos básicos de películas extraídas desde IMDb
-- =============================================
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,               -- Identificador único (autoincremental)
    imdb_id VARCHAR(15) UNIQUE NOT NULL, -- ID oficial de IMDb (ej. tt0111161)
    title TEXT NOT NULL CHECK (char_length(title) > 0), -- Título no vacío
    year INT CHECK (year BETWEEN 1888 AND EXTRACT(YEAR FROM CURRENT_DATE) + 1), -- Rango de años válidos
    rating FLOAT CHECK (rating BETWEEN 0 AND 10), -- Calificación IMDb
    duration_minutes INT CHECK (duration_minutes BETWEEN 1 AND 600), -- Duración razonable (hasta 10 horas)
    metascore INT CHECK (metascore BETWEEN 0 AND 100) -- Puntuación Metacritic
);

-- =============================================
-- Tabla: actors
-- Descripción: Contiene los nombres únicos de los actores principales
-- =============================================
CREATE TABLE actors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (char_length(name) > 1) -- Nombre no vacío y único
);

-- =============================================
-- Tabla: movie_actor
-- Descripción: Representa la relación N:M entre películas y actores
-- =============================================
CREATE TABLE movie_actor (
    movie_id INT NOT NULL,
    actor_id INT NOT NULL,
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES actors(id) ON DELETE CASCADE
);

-- =============================================
-- Índices para consultas más rápidas por año y calificación
-- =============================================
CREATE INDEX idx_movies_year_rating ON movies(year, rating);
