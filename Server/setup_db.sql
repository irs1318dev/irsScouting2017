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


-- backup command for windows
-- if you are logged in
--"C:\Program Files\PostgreSQL\9.6\bin\pg_dump.exe" --file "C:/Users/james/PycharmProjects/irsScouting2017/Server/dbbackup/waamv_2017_with_results.backup" --host "localhost" --port "5432" --username "postgres" --no-password --verbose --role "irs1318" --format=t --blobs --encoding "UTF8" "scouting"

-- if you have not yet logged in
--"C:\Program Files\PostgreSQL\9.6\bin\pg_dump.exe" --file "C:/Users/james/PycharmProjects/irsScouting2017/Server/dbbackup/waamv_2017_with_results.backup" --host "localhost" --port "5432" --username "postgres" --verbose --role "irs1318" --format=t --blobs --encoding "UTF8" "scouting"