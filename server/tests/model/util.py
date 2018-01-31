import os
import os.path
import subprocess

import pandas
import psycopg2.pool
import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.setup as sms
import server.tests.conf as conf


def create_testdb():
    """Creates test database and retrieves sqlalchemy connection engine.

    Creates a test user accounjt if it doesn't already exist.

    Drops the database and closes all connections once all fixture
    dependent tests have finished.

    Args:
        db_params: (dict) Requires database connection parameters

    Returns: (sqlalchemy.Engine) Engine for connecting to test database.
    """
    pool = psycopg2.pool.SimpleConnectionPool(1, 1, dbname=conf.root_db,
                                              host=conf.host,
                                              user=conf.root_user,
                                              password=conf.root_pw)
    conn = pool.getconn()
    conn.autocommit = True
    curr = conn.cursor()

    # Create test user account
    curr.execute("SELECT COUNT(*) FROM pg_roles WHERE rolname = %s;",
                 (conf.test_user, ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE USER " + conf.test_user +
                     " " + "WITH PASSWORD %s CREATEDB;",
                     (conf.test_pw, ))

    # Create test database
    curr.execute("SELECT COUNT(*) FROM pg_database "
                 "WHERE datname = %s", (conf.test_db, ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE DATABASE " + conf.test_db +
                     " OWNER " + conf.test_user + ";")

    curr.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public "
                 "TO " + conf.test_user)
    curr.close()
    conn.close()
    return True


def drop_testdb():
    pool = psycopg2.pool.SimpleConnectionPool(1, 1, dbname=conf.root_db,
                                              host=conf.host,
                                              user=conf.root_user,
                                              password=conf.root_pw)
    conn = pool.getconn()
    conn.autocommit = True
    curr = conn.cursor()
    curr.execute("DROP DATABASE IF EXISTS " + conf.test_db + ";")
    curr.close()
    conn.close()


def verify_testdb():
    conn = smc.pool.getconn()
    assert conn.dsn == ("user=irs1318test password=xxx "
                        "dbname=scouting_test host=localhost")
    conn.close()


def create_empty_tables():
    """ Inserts empty tables into the scouting database.

    The `tables_empty` and `restored_testdb` fixtures should not be
    used simultaneously in the same module. The purpose of
    `tables_empty` is to test database setup routines.

    Args:
        testdb_engine: (sqlalchemy engine)
            Engine for connecting to test database using test account.

    Returns: (Boolean) True
    """
    verify_testdb()
    sms.create_tables()
    return True


# noinspection PyShadowingNames
# @pytest.fixture(scope="module")
# def restored_testdb(db_params, root_psyco_conn, testdb_engine):
#     """
#
#     Args:
#         db_params: (dict) Database parameters
#         root_psyco_conn: (pscypg2 connection object)
#             Connection object that uses postgres superuser account.
#         testdb_conn: (sqlalchemy engine)
#             Sqlalchemy connection engine that uses test user account.
#
#     Returns: (Boolean) True
#     """
#     # Set current Python working directory to folder containing
#     # Postgresql backup file.
#     test_data_path = os.path.join(os.path.dirname(__file__),
#                                   "test_data")
#     os.chdir(test_data_path)
#
#     # Database restore has errors unless user is a superuser.
#     curr = root_psyco_conn.cursor()
#     sql = "ALTER USER " + db_params["test_user"] + " WITH SUPERUSER;"
#     curr.execute(sql)
#
#     # Postgresql restore file (text format) must be created with -O
#     # option (using pg_dump) so it can be restored by any account.
#     db_conn = ("postgresql://" + db_params["test_user"] + ":" +
#                db_params["test_pw"] + "@" + db_params["host"] + ":" +
#                db_params["port"] + "/" + db_params["test_db"])
#     # '> NUL' is shell command that turns off text output
#     cmd = "psql -w " + db_conn + " < turing_2017_0422_1009 > NUL"
#     subprocess.run(cmd, shell=True)
#
#     # For general security, remove superuser permission from account.
#     sql = "ALTER USER " + db_params["test_user"] + " WITH NOSUPERUSER;"
#     curr.execute(sql)
#     curr.close()
#
#     # Verify that all tables were created.
#     sql = ("SELECT table_name FROM information_schema.tables "
#            "WHERE table_schema = 'public';")
#     conn = smc.engine.connect()
#     tables = pandas.read_sql_query(sql, conn)
#     conn.close()
#     assert tables.shape == (19, 1)
#     return True


#
# # noinspection PyShadowingNames
# @pytest.fixture(scope="module")
# def tables_initialized(testdb_engine):
#     """ Inserts tables into database and loads them with initial data.
#
#     Loads initial data into scouting database schema, such as match
#     numbers, actors, phases, etc. This fixture does not load any
#     competition measures.
#
#     Args:
#         testdb_engine: (sqlalchemy engine)
#             Engine for connecting to test database using test account.
#
#     Returns: (Boolean) True
#     """
#     sms.setup()
#     return True
