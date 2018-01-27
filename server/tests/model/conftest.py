import os
import os.path
import subprocess

import pandas
import psycopg2.pool
import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.setup as sms


@pytest.fixture(scope="module")
def db_params():
    """Database connection parameters.

    Returns: Python dictionary containing connection parameters.
    """
    return {"user": "irs1318",
            "pw": "irs1318",
            "root_user": "postgres",
            "root_pw": "irs1318",
            "root_db": "postgres",
            "test_user": "irs1318test",
            "test_pw": "irs1318test",
            "test_db": "scouting_test",
            "host": "localhost",
            "port": "5432"}


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def root_psyco_conn(db_params):
    """Obtains a psycopg2 connection to test db using postgres root account.

    The connection will be closed once the fixture is released.

    Arg:
        db_params: (dict) Database parameters

    Returns: a psycopg2 connection object.
    """
    pool = psycopg2.pool.SimpleConnectionPool(1, 1, dbname=db_params["root_db"],
                                              host=db_params["host"],
                                              user=db_params["root_user"],
                                              password=db_params["root_pw"])
    psyco_conn = pool.getconn()
    psyco_conn.autocommit = True
    yield psyco_conn
    psyco_conn.autocommit = False
    pool.closeall()


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def testdb_engine(db_params, root_psyco_conn):
    """Creates test database and retrieves sqlalchemy connection engine.

    Creates a test user accounjt if it doesn't already exist.

    Drops the database and closes all connections once all fixture
    dependent tests have finished.

    Args:
        db_params: (dict) Requires database connection parameters

    Returns: (sqlalchemy.Engine) Engine for connecting to test database.
    """
    curr = root_psyco_conn.cursor()

    # Create test user account
    curr.execute("SELECT COUNT(*) FROM pg_roles WHERE rolname = %s;",
                 (db_params["test_user"], ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE USER " + db_params["test_user"] +
                     " " + "WITH PASSWORD %s CREATEDB;",
                     (db_params["test_pw"], ))

    # Create test database
    curr.execute("SELECT COUNT(*) FROM pg_database "
                 "WHERE datname = %s", (db_params["test_db"], ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE DATABASE " + db_params["test_db"] +
                     " OWNER " + db_params["test_user"] + ";")

    curr.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public "
                 "TO " + db_params["test_user"])

    conn_str = smc.create_conn_string(user=db_params["test_user"],
                                      password=db_params["test_pw"],
                                      dbname=db_params["test_db"])
    yield smc.reset_engine(conn_str)

    # Teardown code
    smc.engine.dispose()
    curr.execute("DROP DATABASE IF EXISTS " + db_params["test_db"] + ";")
    curr.close()


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def testdb_conn(testdb_engine):
    """Provides a sqlalchemy connection for test database.

    Args:
        testdb_engine: (sqlalchemy engine)
            Engine for connecting to test database using test account.

    Returns: Sqlalchemy engine for connecting to test database using
    test user account.
    """
    assert isinstance(testdb_engine, sqlalchemy.engine.base.Engine)
    conn = testdb_engine.connect()
    yield conn
    conn.close()


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def restored_testdb(db_params, root_psyco_conn, testdb_conn):
    """

    Args:
        db_params: (dict) Database parameters
        root_psyco_conn: (pscypg2 connection object)
            Connection object that uses postgres superuser account.
        testdb_conn: (sqlalchemy engine)
            Sqlalchemy connection engine that uses test user account.

    Returns: (Boolean) True
    """
    # Set current Python working directory to folder containing
    # Postgresql backup file.
    test_data_path = os.path.join(os.path.dirname(__file__),
                                  "test_data")
    os.chdir(test_data_path)

    # Database restore has errors unless user is a superuser.
    curr = root_psyco_conn.cursor()
    sql = "ALTER USER " + db_params["test_user"] + " WITH SUPERUSER;"
    curr.execute(sql)

    # Postgresql restore file (text format) must be created with -O
    # option (using pg_dump) so it can be restored by any account.
    db_conn = ("postgresql://" + db_params["test_user"] + ":" +
               db_params["test_pw"] + "@" + db_params["host"] + ":" +
               db_params["port"] + "/" + db_params["test_db"])
    # '> NUL' is shell command that turns off text output
    cmd = "psql -w " + db_conn + " < turing_2017_0422_1009 > NUL"
    subprocess.run(cmd, shell=True)

    # For general security, remove superuser permission from account.
    sql = "ALTER USER " + db_params["test_user"] + " WITH NOSUPERUSER;"
    curr.execute(sql)
    curr.close()

    # Verify that all tables were created.
    sql = ("SELECT table_name FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, testdb_conn)
    assert tables.shape == (19, 1)
    return True


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def tables_empty(testdb_engine):
    """ Inserts empty tables into the scouting database.

    The `tables_empty` and `restored_testdb` fixtures should not be
    used simultaneously in the same module. The purpose of
    `tables_empty` is to test database setup routines.

    Args:
        testdb_engine: (sqlalchemy engine)
            Engine for connecting to test database using test account.

    Returns: (Boolean) True
    """
    assert isinstance(testdb_engine, sqlalchemy.engine.base.Engine)
    sms.create_tables()
    return True


# noinspection PyShadowingNames
@pytest.fixture(scope="module")
def tables_loaded(testdb_engine):
    """ Inserts tables into database and loads them with initial data.

    Loads initial data into scouting database schema, such as match
    numbers, actors, phases, etc. This fixture does not load any
    competition measures.

    Args:
        testdb_engine: (sqlalchemy engine)
            Engine for connecting to test database using test account.

    Returns: (Boolean) True
    """
    assert isinstance(testdb_engine, sqlalchemy.engine.base.Engine)
    sms.setup()
    return True
