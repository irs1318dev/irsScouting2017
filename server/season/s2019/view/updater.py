import server.model.event as sme
import server.season.s2019.view.rankingtable as r
import server.season.s2019.view.sixteam as s
import server.season.s2019.view.oneteam as o
import server.season.s2019.view.pointschart as p


def update_graph():
    teams = sme.EventDal.last_match_teams()
    # Ranking Table
    update_ranking()
    # Points Chart
    update_points()
    # One Team Chart
    update_one_team(teams)
    # Six Team Chart
    update_six_team()
    # Index Pages
    update_indexes()


def update_ranking():
    r.pages_rankingtable()


def update_one_team(teams):
    o.pages_1t(teams)


def update_six_team():
    s.next3('1318')


def update_points():
    p.pages_pointschart()


def update_indexes():
    s.index_page()
    o.index_page1t()
