import pandas
import sqlalchemy

import server.model.upsert as smu


def test_upsert(tables, db_conn):
    assert tables

    smu.upsert("events", "name", "wairs1")
    smu.upsert("events", "name", "wairs2")

    sql_count = sqlalchemy.text("SELECT COUNT(*) FROM events;")
    count = db_conn.execute(sql_count).scalar()
    assert count == 2

    sql_sel = sqlalchemy.text("SELECT * FROM events;")
    teams = pandas.read_sql_query(sql_sel, db_conn)
    assert teams.shape == (2, 4)
    assert teams.name[0] == "wairs1"

    # Teardown
    delete_all_rows("events", db_conn)


def test_upsert_rows(tables, db_conn):
    assert tables

    smu.upsert_rows("events", "name", 25, "{0:0>3}-q")
    sql = "SELECT * FROM events;"
    matches = pandas.read_sql_query(sql, db_conn)
    assert matches.shape == (24, 4)
    assert matches.name[0] == "001-q"

    # Teardown
    delete_all_rows("events", db_conn)


def test_upsert_cols(tables, db_conn):
    assert tables
    smu.upsert_cols("task_options", {"task_name": "na",
                                     "type": "capability",
                                     "option_name": "na"})
    sql = "SELECT * FROM task_options;"
    tasks = pandas. read_sql_query(sql, db_conn)
    assert tasks.task_name[0] == "na"
    assert tasks.type[0] == "capability"
    assert tasks.option_name[0] == "na"
    assert tasks.shape == (1, 4)

    # Teardown
    delete_all_rows("events", db_conn)


def delete_all_rows(table, db_test_conn):
    sql_drop = "DELETE FROM " + table + ";"
    db_test_conn.execute(sql_drop)