-- Conectarse a la base de datos 'postgres' (o cualquier otra) antes de ejecutar esto

-- Terminar conexiones activas y eliminar la base de datos si existe
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'datawarehouse' AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS datawarehouse;

-- Crear los schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
