-- Database: scouting
-- DROP DATABASE scouting;

CREATE DATABASE scouting
    WITH 
    OWNER = irs1318
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- User: irs1318
-- DROP USER irs1318;

CREATE USER irs1318 WITH
	LOGIN
    SUPERUSER
    INHERIT
    CREATEDB
    CREATEROLE
	REPLICATION;