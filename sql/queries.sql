-- =============================================
--  Archivo: queries.sql
--  Propósito: Consultas analíticas avanzadas sobre la base IMDb
--  Autor: Andrés Ruiz
--  Fecha de creación: 2025-08-03
--  Descripción: Incluye análisis estadístico, comparaciones y ranking
-- =============================================


-- =============================================
-- 1. Top 5 décadas con mayor promedio de duración de películas
-- Objetivo: Identificar en qué décadas se produjeron películas más largas, en promedio.
-- =============================================
SELECT
    (year / 10) * 10 AS decade,
    ROUND(AVG(duration_minutes)::numeric, 2) AS avg_duration
FROM movies
GROUP BY decade
ORDER BY avg_duration DESC
LIMIT 5;


-- =============================================
-- 2. Desviación estándar de las calificaciones IMDb por año
-- Objetivo: Medir la dispersión o variabilidad de calificaciones dentro de cada año.
-- =============================================
SELECT
    year,
    COUNT(*) AS total_movies,
    ROUND(STDDEV(rating)::numeric, 3) AS rating_stddev
FROM movies
WHERE rating IS NOT NULL
GROUP BY year
ORDER BY year;


-- =============================================
-- 3. Películas con diferencia >20% entre calificación IMDb y Metascore normalizado (0-10)
-- Objetivo: Detectar películas con opiniones divididas entre público (IMDb) y crítica (Metascore).
-- =============================================
SELECT
    title,
    rating AS imdb_rating,
    metascore / 10.0 AS metascore_normalized,
    ROUND(ABS(rating - metascore / 10.0)::numeric, 2) AS difference,
    ROUND((ABS(rating - metascore / 10.0) / rating)::numeric * 100, 2) AS diff_percentage
FROM movies
WHERE metascore IS NOT NULL AND rating IS NOT NULL
  AND (ABS(rating - metascore / 10.0) / rating) > 0.2;


-- =============================================
-- 4. Ranking por año de las películas usando funciones de ventana
-- Objetivo: Obtener el top de películas mejor calificadas por año.
-- =============================================
SELECT
    year,
    title,
    rating,
    RANK() OVER (PARTITION BY year ORDER BY rating DESC) AS rank_in_year
FROM movies
ORDER BY year, rank_in_year;
