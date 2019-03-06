import server.model.event as sme
import server.season.s2019.view.rankingtable as r
import server.season.s2019.view.sixteam as s
import server.season.s2019.view.oneteam as o
import server.season.s2019.view.pointschart as p


def update_graph():
    teams = sme.EventDal.last_match_teams()
    r.pages_rankingtable()
    o.pages_1t(teams)
    s.next3('1318')
    p.pages_pointschart()
    s.index_page()
    o.index_page1t()
