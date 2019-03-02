import server.model.event as sme
import server.season.s2019.view.updater as u


def test_updater():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('030-q')
    u.update_graph()
