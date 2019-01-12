import server.model.event as sme


def test_get_status():
    print(sme.EventDal.get_current_status())

def test_set_event():
    sme.EventDal.set_current_event("wayak", "2018")
