-- =============================================
--  Archivo: views.sql
--  Propósito: Crear vistas relacionales para facilitar consultas de películas y actores
--  Autor: Andrés Ruiz
--  Fecha de creación: 2025-08-03
--  Descripción: Vista que relaciona cada película con su actor principal
-- =============================================

-- =============================================
-- VIEW: vw_movie_actor_main
-- Descripción: Muestra, por cada película, el actor con ID más bajo (considerado principal).
-- Útil para reportes simplificados que requieren solo un actor por película.
-- =============================================
CREATE OR REPLACE VIEW vw_movie_actor_main AS
SELECT
    m.id AS movie_id,
    m.title,
    a.id AS actor_id,
    a.name AS actor_name
FROM movies m
JOIN movie_actor ma ON m.id = ma.movie_id
JOIN actors a ON ma.actor_id = a.id
WHERE ma.actor_id = (
    SELECT MIN(ma2.actor_id)
    FROM movie_actor ma2
    WHERE ma2.movie_id = m.id
);
