"""Tests database update and setup code.

Tests code in following modules:
    * server.model.update.py
    * server.model.setup.py
"""

import pandas


def test_tables(tables_loaded, db_conn):
    assert tables_loaded
    sql = ("SELECT * FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, db_conn)
    assert tables.shape == (19, 12)

    def test_table(table, shape):
        sql = "SELECT * FROM " + table + ";"
        dframe = pandas.read_sql_query(sql, db_conn)
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








