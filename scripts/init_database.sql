-- Ejecutar conectado a 'postgres'

DROP DATABASE IF EXISTS DataWarehouse;
CREATE DATABASE DataWarehouse;

-- Luego conectarte manualmente a DataWarehouse

-- Crear schemas
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
