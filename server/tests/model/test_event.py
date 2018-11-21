import server.model.event as sme


def test_get_status():
    print(sme.EventDal.get_current_status())
