import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.setup as sms
from server.model import setup as sms


@pytest.fixture
def db_params():
    return {"user": "irs1318",
            "pw": "irs1318",
            "root_user": "postgres",
            "root_pw": "irs1318",
            "test_user": "irs1318test",
            "test_pw": "irs1318test",
            "test_db": "scouting_test"}


@pytest.fixture
def db_engine(db_params):
    # Create engine using root db account
    root_conn_str = smc.create_conn_string(user=db_params["root_user"],
                                           password=db_params["root_pw"])
    root_engine = sqlalchemy.create_engine(root_conn_str)

    # Create test user account
    sql_user_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_roles "
                                     "WHERE rolname = :usr;")
    res = root_engine.execute(sql_user_check,
                              usr=db_params["test_user"])
    if not res.scalar():
        sql_user = sqlalchemy.text("CREATE USER " + db_params["test_user"] +
                                   " " + "WITH PASSWORD :pw CREATEDB;" )
        root_engine.execute(sql_user, pw=db_params["test_pw"])

    # Create test database
    sql_db_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_database "
                                   "WHERE datname = :testdb")
    res = root_engine.execute(sql_db_check, testdb=db_params["test_db"])

    conn = root_engine.connect()
    if not res.scalar():
        sql_db = sqlalchemy.text("CREATE DATABASE " + db_params["test_db"] +
                                 " OWNER " + db_params["test_user"] + ";")
        # root_engine.execute doesn't work for creating databases.
        conn.execute("commit")
        conn.execute(sql_db)

    conn_str = smc.create_conn_string(user=db_params["test_user"],
                                      password=db_params["test_pw"],
                                      dbname=db_params["test_db"])
    yield smc.reset_engine(conn_str)

    # Teardown code
    smc.engine.dispose()

    sql_drop = ("DROP DATABASE IF EXISTS " + db_params["test_db"] + ";")
    conn.execute("commit")
    conn.execute(sql_drop)
    conn.close()
    root_engine.dispose()


@pytest.fixture
def db_conn(db_engine):
    conn = db_engine.connect()
    yield conn
    conn.close()


@pytest.fixture
def tables(db_engine):
    assert isinstance(db_engine, sqlalchemy.engine.base.Engine)
    sms.create_tables()
    return True


@pytest.fixture
def tables_loaded(db_conn):
    print(type(db_conn))
    sms.setup()
    return True