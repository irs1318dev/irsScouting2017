import sqlalchemy

import server.model.version as sm_version
import server.model.connection as sm_connection


def test_get_version():
    assert sm_version.get_version() == "2018.02"


def test_ver2018_02():
    sm_version.set_ver_2018_02()

def test_remove_constraint():
    conn = sm_connection.engine.connect()
    sql = sqlalchemy.text("ALTER TABLE events DROP CONSTRAINT events_name_key;")
    conn.execute(sql)