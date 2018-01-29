"""Tests database update and setup code.

Tests code in following modules:
    * server.model.update.py
    * server.model.setup.py
"""

import pandas
import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.setup as sms
import server.tests.conf as conf
import server.tests.model.util as util


@pytest.fixture(scope="module")
def testdb_initialized_tables():
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


def test_tables(testdb_initialized_tables):
    assert testdb_initialized_tables
    util.verify_testdb()
    sms.setup()

    conn = smc.engine.connect()
    sql = ("SELECT * FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, conn)
    assert tables.shape == (19, 12)

    def test_table(table, shape):
        sql = "SELECT * FROM " + table + ";"
        dframe = pandas.read_sql_query(sql, conn)
        assert dframe.shape == shape

    test_table("levels", (3, 2))
    test_table("matches", (168, 2))
    test_table("alliances", (3, 2))
    test_table("dates", (1, 3))
    test_table("teams", (1, 7))
    test_table("stations", (4, 2))
    test_table("actors", (7, 2))
    test_table("tasks", (92, 4))
    test_table("measuretypes", (7, 2))
    test_table("phases", (5, 2))
    test_table("attempts", (31, 2))
    test_table("reasons", (4, 2))
    test_table("task_options", (88, 4))
