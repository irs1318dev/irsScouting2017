import server.model.event as sme
import server.season.s2019.view.oneteam as oneteam


def test_plot():
    sme.EventDal.set_current_event('wamou', '2019')
    sme.EventDal.set_current_match('030-q')
    teams = sme.EventDal.last_match_teams()
    oneteam.pages_1t(teams)


def test_indexpage():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('030-q')
    teams = sme.EventDal.last_match_teams()
    oneteam.index_page1t()

