SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE DATNAME = 'datawarehouse' AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS datawarehouse;

CREATE DATABASE datawarehouse;

CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
