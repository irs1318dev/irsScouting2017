import server.model.event as sme
import server.season.s2019.view.oneteam as oneteam


def test_plot():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('030-q')
    teams = ['360', '3223']
    oneteam.pages_1t(teams)
