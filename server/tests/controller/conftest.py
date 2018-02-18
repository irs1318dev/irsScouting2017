import pytest
import sqlalchemy

import server.model.connection as sm_connection
import server.model.dal as sm_dal
import server.model.event as sm_event
import server.tests.conf as st_conf


@pytest.fixture(scope="module")
def test_event():
    event_id = sm_event.EventDal.set_current_event(st_conf.test_event[0],
                                                   st_conf.test_event[1])
    conn = sm_connection.engine.connect()
    sql_sel = sqlalchemy.text("SELECT * FROM status WHERE event_id = :evt_id;")
    results = conn.execute(sql_sel, evt_id=event_id)
    assert results.rowcount == 1
    yield results.fetchone()
    results.close()
    conn = sm_connection.engine.connect()
    sql_del = sqlalchemy.text("DELETE FROM measures WHERE event_id = :evt_id;")
    conn.execute(sql_del, evt_id=event_id)
    sql_del = sqlalchemy.text("DELETE FROM events WHERE id = :evt_id;")
    conn.execute(sql_del, evt_id=event_id)
    conn.close()
    sm_event.EventDal.set_current_event(st_conf.def_event[0],
                                        st_conf.def_event[1])