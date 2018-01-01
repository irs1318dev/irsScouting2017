import pytest
import sqlalchemy
import pandas

import server.model.connection as smc
import server.model.setup_database as sms
import server.model.update


@pytest.fixture
def db_test_engine():
    TEST_USER = "irs1318test"
    TEST_PW = "irs1318test"
    TEST_DB = "scouting_test"

    # Create engine using root db account
    root_conn_str = smc.create_conn_string(user="postgres",
                                           password="irs1318")
    root_engine = sqlalchemy.create_engine(root_conn_str)

    # Create test user account
    sql_user_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_roles "
                                     "WHERE rolname = :usr;")
    res = root_engine.execute(sql_user_check, usr=TEST_USER)
    if not res.scalar():
        sql_user = sqlalchemy.text("CREATE USER " + TEST_USER + " " +
                                   "WITH PASSWORD :pw CREATEDB;" )
        root_engine.execute(sql_user, pw=TEST_PW)

    sql_db_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_database "
                                   "WHERE datname = :testdb")
    res = root_engine.execute(sql_db_check, testdb=TEST_DB)
    if not res.scalar():
        sql_db = sqlalchemy.text("CREATE DATABASE " + TEST_DB +
                                 " OWNER " + TEST_USER + ";")
        # root_engine.execute doesn't work for creating databases.
        conn = root_engine.connect()
        conn.execute("commit")
        conn.execute(sql_db)

    root_engine.dispose()

    conn_str = smc.create_conn_string(user=TEST_USER, password=TEST_PW,
                                      dbname=TEST_DB)
    return sqlalchemy.create_engine(conn_str)


def test_table_creation(db_test_engine):
    assert isinstance(db_test_engine, sqlalchemy.engine.base.Engine)
    conn = db_test_engine.connect()

    sms.create_tables(db_test_engine)
    sql = ("SELECT * FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, conn)
    assert tables.shape == (19, 12)


@pytest.fixture
def db_conn():
    return server.model.connection.engine.connect()


def test_upsert(db_conn):
    sql_del = sqlalchemy.text("DELETE FROM test_dimension;")
    db_conn.execute(sql_del)

    server.model.update.upsert("test_dimension", "name", "testVal1")
    server.model.update.upsert("test_dimension", "name", "testVal2")

    sql_count = sqlalchemy.text("SELECT COUNT(*) FROM test_dimension;")
    count = db_conn.execute(sql_count).scalar()
    assert count == 2

    sql_sel = sqlalchemy.text("SELECT * FROM test_dimension;")
    results = db_conn.execute(sql_sel)
    for row in results:
        print(row)

    db_conn.execute(sql_del)
    count = db_conn.execute(sql_count).scalar()
    assert count == 0






