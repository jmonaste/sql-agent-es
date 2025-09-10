-- Inicialización automática de la base de datos SAKILA en español
-- Este script se ejecuta automáticamente cuando se levanta el contenedor

-- Mensaje informativo
SELECT 'Inicializando base de datos SAKILA en español...' AS mensaje;

-- Ejecutar esquema de la base de datos en español
SOURCE /docker-entrypoint-initdb.d/sakila-schema-spanish.sql;

-- Ejecutar datos de la base de datos en español
SOURCE /docker-entrypoint-initdb.d/sakila-data-spanish.sql;

SELECT 'Base de datos SAKILA en español lista para usar' AS mensaje;