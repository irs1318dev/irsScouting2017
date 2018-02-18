import pandas
import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.event as sme
import server.model.upsert as smu
import server.tests.conf as conf
import server.tests.model.util as util


@pytest.fixture(scope="module")
def testdb_empty_tables():
    util.create_testdb()
    conn_str = smc.create_conn_string(user=conf.test_user,
                                      password=conf.test_pw,
                                      dbname=conf.test_db)
    smc.engine = sqlalchemy.create_engine(conn_str)
    smc.pool = smc.set_pool(dbname=conf.test_db, user=conf.test_user,
                            password=conf.test_pw)
    util.create_empty_tables()
    yield True
    smc.engine.dispose()
    smc.pool.closeall()
    util.drop_testdb()


# noinspection PyShadowingNames
def test_upsert(testdb_empty_tables):
    assert testdb_empty_tables
    util.verify_testdb()
    conn = smc.engine.connect()

    smu.upsert("actors", "name", "upsert_test1")
    smu.upsert("actors", "name", "upsert_test2")

    sql_count = sqlalchemy.text("SELECT COUNT(*) FROM actors;")
    count = conn.execute(sql_count).scalar()
    assert count == 2

    sql_sel = "SELECT * FROM actors;"
    actors = pandas.read_sql_query(sql_sel, conn)
    assert actors.shape == (2, 2)
    assert actors.name[0] == "upsert_test1"

    # Teardown
    delete_all_rows("actors", conn)
    conn.close()


# noinspection PyShadowingNames
def test_upsert_rows(testdb_empty_tables):
    assert testdb_empty_tables
    util.verify_testdb()

    conn = smc.engine.connect()
    smu.upsert_rows("matches", "name", 25, "{0:0>3}-q")
    sql = "SELECT * FROM matches;"
    matches = pandas.read_sql_query(sql, conn)
    assert matches.shape == (24, 2)
    assert matches.name[0] == "001-q"

    # Teardown
    delete_all_rows("matches", conn)
    conn.close()


# noinspection PyShadowingNames
def test_upsert_cols(testdb_empty_tables):
    assert testdb_empty_tables
    util.verify_testdb()

    conn = smc.engine.connect()
    smu.upsert_cols("task_options", {"task_name": "na",
                                     "type": "capability",
                                     "option_name": "na"})
    sql = "SELECT * FROM task_options;"
    tasks = pandas. read_sql_query(sql, conn)
    assert tasks.task_name[0] == "na"
    assert tasks.type[0] == "capability"
    assert tasks.option_name[0] == "na"
    assert tasks.shape == (1, 4)

    # Teardown
    delete_all_rows("task_options", conn)
    conn.close()


def delete_all_rows(table, conn):
    print("Deleting table " + table)
    sql_delete = "DELETE FROM " + table + ";"
    conn.execute(sql_delete)