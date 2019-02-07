import server.model.event as sme

def test_team_names():
    team = '3586'
    recent = sme.EventDal.team_long_name(team)
    assert recent == 'Pride in the Tribe-Caveman Robotics'
    team = '2046'
    recent2 = sme.EventDal.team_long_name(team)
    assert recent2 == 'Bear Metal'
    team = '1318'
    recent3 = sme.EventDal.team_long_name(team)
    assert recent3 == 'Issaquah Robotics Society'
    team = '4911'
    recent4 = sme.EventDal.team_long_name(team)
    assert recent4 == 'CyberKnights'
    team = '3681'
    recent5 = sme.EventDal.team_long_name(team)
    assert recent5 == 'na'
