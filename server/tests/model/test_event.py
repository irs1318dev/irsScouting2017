import server.model.event as sme

def test_get_previous_match():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('029-q')
    assert sme.EventDal.get_previous_match() == '028-q'
    sme.EventDal.set_current_match('112-q')
    assert sme.EventDal.get_previous_match() == '111-q'
    sme.EventDal.set_current_match('002-q')
    assert sme.EventDal.get_previous_match()
    sme.EventDal.set_current_match('001-q')
    assert sme.EventDal.get_previous_match() == '001-q'
    sme.EventDal.set_current_match('030-q')


def test_last_match_teams():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('029-q')
    assert sme.EventDal.last_match_teams() == ['949', '6350', '2976',
                                               '4131', '3684', '2906']


def test_team_match():
    sme.EventDal.set_current_event('test_data', '2019')
    sme.EventDal.set_current_match('029-q')
    print(sme.EventDal.team_match('1318'))


