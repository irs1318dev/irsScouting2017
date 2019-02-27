import server.model.event as sme
import server.season.s2019.view.rankingtable as r
import server.season.s2019.view.sixteam as s
import server.season.s2019.view.oneteam as o


def update_graph():
    teams = sme.EventDal.last_match_teams()
    r.pages_rankingtable()
    s.pages_6t(sme.EventDal.get_current_match())
    o.pages_1t(teams)

