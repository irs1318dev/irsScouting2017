import server.model.event as sme
import server.season.s2019.view.oneteam as o
import server.season.s2019.view.sixteam as s
import server.season.s2019.view.rankingtable as r
import server.model.event as sme


def update_graphs():
    match = sme.EventDal.get_previous_match()
    teams = sme.EventDal.last_match_teams()
    r.pages_rankingtable()
    s.pages_6t(match)
    for team in teams:
        o.pages_1t(team)
