import pandas
import pytest
import sqlalchemy

import server.model.update as smu
import server.model.connection as smc
import server.model.setup as sms

TEST_USER = "irs1318test"
TEST_PW = "irs1318test"
TEST_DB = "scouting_test"


@pytest.fixture
def db_test_engine():
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

    # Create test database
    sql_db_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_database "
                                   "WHERE datname = :testdb")
    res = root_engine.execute(sql_db_check, testdb=TEST_DB)

    conn = root_engine.connect()
    if not res.scalar():
        sql_db = sqlalchemy.text("CREATE DATABASE " + TEST_DB +
                                 " OWNER " + TEST_USER + ";")
        # root_engine.execute doesn't work for creating databases.
        conn.execute("commit")
        conn.execute(sql_db)

    conn_str = smc.create_conn_string(user=TEST_USER, password=TEST_PW,
                                      dbname=TEST_DB)
    yield smc.reset_engine(conn_str)

    # Teardown code
    smc.engine.dispose()

    sql_drop = ("DROP DATABASE IF EXISTS " + TEST_DB + ";")
    conn.execute("commit")
    conn.execute(sql_drop)
    conn.close()
    root_engine.dispose()


@pytest.fixture
def db_test_conn(db_test_engine):
    conn = db_test_engine.connect()
    yield conn
    conn.close()


@pytest.fixture
def tables(db_test_engine):
    assert isinstance(db_test_engine, sqlalchemy.engine.base.Engine)
    sms.create_tables()
    return True


def test_upsert(tables, db_test_conn):
    assert tables

    smu.upsert("events", "name", "wairs1")
    smu.upsert("events", "name", "wairs2")

    sql_count = sqlalchemy.text("SELECT COUNT(*) FROM events;")
    count = db_test_conn.execute(sql_count).scalar()
    assert count == 2

    sql_sel = sqlalchemy.text("SELECT * FROM events;")
    teams = pandas.read_sql_query(sql_sel, db_test_conn)
    assert teams.shape == (2, 4)
    assert teams.name[0] == "wairs1"

    # Teardown
    delete_all_rows("events", db_test_conn)


def test_upsert_rows(tables, db_test_conn):
    assert tables

    smu.upsert_rows("events", "name", 25, "{0:0>3}-q")
    sql = "SELECT * FROM events;"
    matches = pandas.read_sql_query(sql, db_test_conn)
    assert matches.shape == (24, 4)
    assert matches.name[0] == "001-q"

    # Teardown
    delete_all_rows("events", db_test_conn)


def test_upsert_cols(tables, db_test_conn):
    assert tables
    smu.upsert_cols("task_options", {"task_name": "na",
                                     "type": "capability",
                                     "option_name": "na"})
    sql = "SELECT * FROM task_options;"
    tasks = pandas. read_sql_query(sql, db_test_conn)
    assert tasks.task_name[0] == "na"
    assert tasks.type[0] == "capability"
    assert tasks.option_name[0] == "na"
    assert tasks.shape == (1, 4)

    # Teardown
    delete_all_rows("events", db_test_conn)


def delete_all_rows(table, db_test_conn):
    sql_drop = "DELETE FROM " + table + ";"
    db_test_conn.execute(sql_drop)