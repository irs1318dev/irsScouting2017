import server.model.event as sm_event


def test_list_events():
    events = sm_event.EventDal.list_events()
    print("\n", events)
    assert isinstance(events, list)
    assert len(events) == 11

