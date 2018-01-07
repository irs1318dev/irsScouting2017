import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.setup as sms


@pytest.fixture(scope="module")
def db_params():
    return {"user": "irs1318",
            "pw": "irs1318",
            "root_user": "postgres",
            "root_pw": "irs1318",
            "root_db": "postgres",
            "test_user": "irs1318test",
            "test_pw": "irs1318test",
            "test_db": "scouting_test"}


@pytest.fixture(scope="module")
def db_engine(db_params):
    # Create pyscopg2 connection and cursor
    smc.pool = smc.set_pool(user=db_params["root_user"],
                            password=db_params["root_pw"],
                            dbname=db_params["root_db"])
    psyco_conn = smc.pool.getconn()

    # Necessary for creating new database
    psyco_conn.autocommit = True

    curr = psyco_conn.cursor()

    # Create test user account
    curr.execute("SELECT COUNT(*) FROM pg_roles WHERE rolname = %s;",
                 (db_params["test_user"], ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE USER " + db_params["test_user"] +
                     " " + "WITH PASSWORD %s CREATEDB;",
                     (db_params["test_pw"], ) )

    # Create test database
    curr.execute("SELECT COUNT(*) FROM pg_database "
                 "WHERE datname = %s", (db_params["test_db"], ))

    if not curr.fetchone()[0]:
        curr.execute("CREATE DATABASE " + db_params["test_db"] +
                     " OWNER " + db_params["test_user"] + ";")

    conn_str = smc.create_conn_string(user=db_params["test_user"],
                                      password=db_params["test_pw"],
                                      dbname=db_params["test_db"])
    yield smc.reset_engine(conn_str)

    # Teardown code
    smc.engine.dispose()
    curr.execute("DROP DATABASE IF EXISTS " + db_params["test_db"] + ";")
    curr.close()
    psyco_conn.close()


@pytest.fixture(scope="module")
def db_conn(db_engine):
    conn = db_engine.connect()
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def tables(db_engine):
    assert isinstance(db_engine, sqlalchemy.engine.base.Engine)
    sms.create_tables()
    return True


@pytest.fixture(scope="module")
def tables_loaded(db_conn):
    print(type(db_conn))
    sms.setup()
    return True