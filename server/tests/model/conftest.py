import pytest
import sqlalchemy

import server.model.connection as sm_connection
import server.model.dal as sm_dal
import server.model.event as sm_event
import server.tests.conf as st_conf


@pytest.fixture(scope="module")
def test_event():
    sm_event.EventDal.set_current_event(st_conf.test_event, "2017")
    conn = sm_connection.engine.connect()
    sql_sel = sqlalchemy.text("SELECT * FROM status WHERE event = :evt;")
    results = conn.execute(sql_sel, evt=st_conf.test_event)
    assert results.rowcount == 1
    yield results.fetchone()
    results.close()
    conn = sm_connection.engine.connect()
    sql_del = sqlalchemy.text("DELETE FROM measures WHERE event_id = :evt;")
    conn.execute(sql_del, evt=sm_dal.event_ids[st_conf.test_event])
    sql_del = sqlalchemy.text("DELETE FROM events WHERE name = :evt;")
    conn.execute(sql_del, evt=st_conf.test_event)
    sql_del = sqlalchemy.text("UPDATE status SET event = :evt;")
    conn.execute(sql_del, evt=st_conf.def_event)
    conn.close()