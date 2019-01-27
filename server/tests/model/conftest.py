import pytest
import sqlalchemy

import server.model.connection as sm_connection
import server.model.event as sm_event
import server.tests.conf as st_conf
import server.model.random_data as smr

test_event_name = "pytest"
test_season = "2018"

@pytest.fixture(scope="module")
def test_event():
    prior_event = sm_event.EventDal.get_current_event()
    smr.create_event(test_event_name, test_season, "wayak", "2018")
    event_id = sm_event.EventDal.set_current_event(test_event_name, test_season)
    conn = sm_connection.engine.connect()
    sql_sel = sqlalchemy.text("SELECT * FROM status WHERE event_id = :evt_id;")
    results = conn.execute(sql_sel, evt_id=event_id)
    assert results.rowcount == 1
    yield results.fetchone()
    results.close()
    # conn = sm_connection.engine.connect()
    sql_del = sqlalchemy.text("DELETE FROM measures WHERE event_id = :evt_id;")
    conn.execute(sql_del, evt_id=event_id)
    sql_del = sqlalchemy.text("DELETE FROM events WHERE id = :evt_id;")
    conn.execute(sql_del, evt_id=event_id)
    conn.close()
    sm_event.EventDal.set_current_event(st_conf.def_event[0],
                                        st_conf.def_event[1])

@pytest.fixture(scope="module")
def test_event2():
    """Creates a test event.

    Creates an event called "pytest" for season "2018" and makes this
    the current event in the scouting system. Deletes this event at the
    end of all tests that use this fixture.

    Returns: Tuple consisting event_id, event name, and season.
    """
    prior_event = sm_event.EventDal.get_current_event()
    smr.create_event(test_event_name, test_season, "wayak", "2018")
    sm_event.EventDal.set_current_event(test_event_name, test_season)
    test_event = sm_event.EventDal.get_current_event()
    yield test_event
    conn = sm_connection.engine.connect()
    sql_del = sqlalchemy.text("DELETE FROM measures WHERE event_id = :evt_id;")
    conn.execute(sql_del, evt_id=test_event[0])
    sql_del = sqlalchemy.text("DELETE FROM events WHERE id = :evt_id;")
    conn.execute(sql_del, evt_id=test_event[0])
    sql_del = sqlalchemy.text("DELETE FROM schedules WHERE id = :evt_id;")
    conn.execute(sql_del, evt_id=test_event[0])
    conn.close()
    sm_event.EventDal.set_current_event(prior_event[1],
                                        prior_event[2])
