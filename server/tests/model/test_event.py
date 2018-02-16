import server.model.event as sm_event
import server.model.connection as sm_conn
import sqlalchemy


def test_list_events():
    events = sm_event.EventDal.list_events()
    print("\n", events)
    assert isinstance(events, list)
    assert len(events) == 11

def test_get_current_event():
    conn = sm_conn.engine.connect()
    sql = sqlalchemy.text("SELECT status.event, events.season "
                          "FROM status INNER JOIN events ON status.event = events.name;")
    event = conn.execute(sql)
    for row in event:
        print(row)
    conn.close()
    print(event)

def test_set_current_event():
    conn = sm_conn.engine.connect()
    sm_event.EventDal.set_current_event('turing', '2017')
    #sql = sqlalchemy.text("SELECT * FROM events;")
    #event = conn.execute(sql)
    #sql = sqlalchemy.text("SELECT * FROM status")
    #other = conn.execute(sql)
    event = sm_event.EventDal.set_current_event('turing', '2017')
    #other =
    #assert event =

