import pandas
import pytest
import sqlalchemy

import server.model.connection as smc
import server.model.upsert as smu
import server.tests.conf as conf
import server.tests.model.util as util


# @pytest.fixture(scope="module")
# def testdb_empty_tables():
#     util.create_testdb()
#     conn_str = smc.create_conn_string(user=conf.test_user,
#                                       password=conf.test_pw,
#                                       dbname=conf.test_db)
#     smc.engine = sqlalchemy.create_engine(conn_str)
#     smc.pool = smc.set_pool(dbname=conf.test_db, user=conf.test_user,
#                             password=conf.test_pw)
#     util.create_empty_tables()
#     yield True
#     smc.engine.dispose()
#     # smc.pool.closeall()
#     util.drop_testdb()


# noinspection PyShadowingNames
def test_upsert():
    '''Verifies upsert function inserts data into database

    Also verifies upsert() does not error when reinserting the same
    data.
    '''

    # Run upsert commands
    smu.upsert("actors", "name", "upsert_test1")
    smu.upsert("actors", "name", "upsert_test2")

    # Verify two records in database
    conn = smc.pool.getconn()
    curr = conn.cursor()
    sql = r'''
        SELECT COUNT(*) FROM actors
        WHERE name LIKE 'upsert\_test%';
    '''
    curr.execute(sql)
    assert curr.fetchone()[0] == 2

    # Run upsert commands again to ensure no errors if inserting
    #   data that already exists
    smu.upsert("actors", "name", "upsert_test1")
    smu.upsert("actors", "name", "upsert_test2")

    # Delete the test data that was just entered
    sql = r'''
        DELETE FROM actors
        WHERE name LIKE 'upsert\_test%';
    '''
    curr.execute(sql)
    conn.commit()

    # Verify test data was deleted
    sql = r'''
        SELECT COUNT(*) FROM actors
        WHERE name LIKE 'upsert\_test%';
    '''
    curr.execute(sql)
    assert curr.fetchone()[0] == 0

    # Release connection
    curr.close()
    smc.pool.putconn(conn)


# noinspection PyShadowingNames
def test_upsert_rows():
    '''Test upsert_rows(), which inserts multiple rows into table.
    '''
    conn = smc.pool.getconn()
    smu.upsert_rows("alliances", "name", 25, "{0:0>3}-q")
    sql = '''
        SELECT * FROM alliances
        WHERE name LIKE '%-q'
        ORDER BY name;
    '''
    test_data = pandas.read_sql(sql, conn)
    assert test_data.shape == (24, 2)
    assert test_data.name[0] == "001-q"

    # Remove test data
    sql='''
        DELETE FROM alliances
        WHERE name LIKE '%-q';
    '''
    curr = conn.cursor()
    curr.execute(sql)
    conn.commit()

    sql = '''
        SELECT COUNT(*) FROM alliances
        WHERE name LIKE '%-q';
    '''
    curr.execute(sql)
    assert curr.fetchone()[0] == 0

    # Teardown
    smc.pool.putconn(conn)


# noinspection PyShadowingNames
def test_upsert_cols():
    smu.upsert_cols("events", {"name": "upsert_test",
                                     "season": "test"})

    conn = smc.pool.getconn()
    curr = conn.cursor()
    sql = '''
        SELECT name, season FROM events
        WHERE name = 'upsert_test';
    '''
    curr.execute(sql)
    assert curr.fetchone()[1] == 'test'

    # Delete test data
    sql = '''
        DELETE FROM events
        WHERE name = 'upsert_test';
    '''
    curr.execute(sql)
    conn.commit()

    sql = '''
        SELECT COUNT(*) FROM events
        WHERE name = 'upsert_test';
    '''
    curr.execute(sql)
    assert curr.fetchone()[0] == 0

    # Teardown
    smc.pool.putconn(conn)

#
# def delete_all_rows(table, conn):
#     print("Deleting table " + table)
#     sql_delete = "DELETE FROM " + table + ";"
#     conn.execute(sql_delete)