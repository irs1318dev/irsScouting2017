"""Tests database update and setup code.

Tests code in following modules:
    * server.model.update.py
    * server.model.setup.py
"""
import pytest
import sqlalchemy
import pandas

import server.model.connection as smc
import server.model.setup as sms
import server.model.update as smu

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

    root_engine.dispose()

    conn_str = smc.create_conn_string(user=TEST_USER, password=TEST_PW,
                                      dbname=TEST_DB)
    db_test_engine = sqlalchemy.create_engine(conn_str)
    yield db_test_engine

    # Teardown code
    db_test_engine.dispose()

    sql_drop = ("DROP DATABASE IF EXISTS " + TEST_DB + ";")
    conn.execute("commit")
    conn.execute(sql_drop)


@pytest.fixture
def tables(db_test_engine):
    assert isinstance(db_test_engine, sqlalchemy.engine.base.Engine)
    conn = db_test_engine.connect()
    sms.setup(db_test_engine)
    conn.close()
    return True


def test_tables(tables, db_test_engine):
    assert tables
    sql = ("SELECT * FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, db_test_engine)
    assert tables.shape == (19, 12)

    def test_table(table, shape):
        sql = "SELECT * FROM " + table + ";"
        dframe = pandas.read_sql_query(sql, db_test_engine)
        assert dframe.shape == shape

    test_table("levels", (3, 2))
    test_table("matches", (168, 2))
    test_table("alliances", (3, 2))
    test_table("dates", (1, 3))
    test_table("teams", (1, 7))
    test_table("stations", (4, 2))
    test_table("actors", (7, 2))
    test_table("tasks", (1, 4))
    test_table("measuretypes", (7, 2))
    test_table("phases", (5, 2))
    test_table("attempts", (31, 2))
    test_table("reasons", (4, 2))


def test_upsert(tables, db_test_engine):
    assert tables

    smu.upsert("events", "name", "wairs1", db_test_engine)
    smu.upsert("events", "name", "wairs2", db_test_engine)

    sql_count = sqlalchemy.text("SELECT COUNT(*) FROM events;")
    count = db_test_engine.execute(sql_count).scalar()
    assert count == 2

    sql_sel = sqlalchemy.text("SELECT * FROM events;")
    teams = pandas.read_sql_query(sql_sel, db_test_engine)
    assert teams.shape == (2, 4)
    assert teams.name[0] == "wairs1"

    # Teardown
    delete_all_rows("events", db_test_engine)


def test_upsert_rows(tables, db_test_engine):
    assert tables

    smu.upsert_rows("events", "name", 25, "{0:0>3}-q", db_test_engine)
    sql = "SELECT * FROM events;"
    matches = pandas.read_sql_query(sql, db_test_engine)
    assert matches.shape == (24, 4)
    assert matches.name[0] == "001-q"

    # Teardown
    delete_all_rows("schedules", db_test_engine)


def test_upsert_cols(tables, db_test_engine):
    assert tables
    smu.upsert_cols("task_options", {"task_name": "startingLocation",
                                     "type": "capability",
                                     "option_name": "retrieval"},
                    db_test_engine)
    sql = "SELECT * FROM task_options;"
    tasks = pandas. read_sql_query(sql, db_test_engine)
    assert tasks.task_name[0] == "startingLocation"
    assert tasks.type[0] == "capability"
    assert tasks.option_name[0] == "retrieval"
    assert tasks.shape == (1, 4)

    # Teardown
    delete_all_rows("task_options", db_test_engine)


def delete_all_rows(table, engine):
    sql_drop = "DELETE FROM " + table + ";"
    engine.execute(sql_drop)






