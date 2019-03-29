import os.path
import os

import server.season.s2019.view.sixteam as sixteam
import server.model.event as sme
import server.season.s2019.view.oneteam as oneteam
import server.season.s2019.view.pointschart as pointschart
import server.season.s2019.view.updater as updater


# Test takes too long to run (generates 12 charts)
# def test_sixteam():
#     sme.EventDal.set_current_event('test_data', '2019')
#     sme.EventDal.set_current_match('030-q')
#     sixteam.pages_6t(sme.EventDal.team_match('1318'))


def test_points_chart():
    sme.EventDal.set_current_event('wayak', '2019')
    sme.EventDal.set_current_match('060-q')
    pointschart.pages_pointschart()


def test_next3():
    # sme.EventDal.set_current_event('test_data', '2019')
    # sme.EventDal.set_current_match('030-q')
    sme.EventDal.set_current_event('wayak', '2019')
    sme.EventDal.set_current_match('040-q')
    sixteam.next3('1318')


def test_index_page():
    sixteam.index_page()


def test_oneteam():
    # sme.EventDal.set_current_event('test_data', '2019')
    # sme.EventDal.set_current_match('030-q')
    teams = sme.EventDal.last_match_teams()
    oneteam.pages_1t(teams)


def test_updater():
    sme.EventDal.set_current_event('wayak', '2019')
    sme.EventDal.set_current_match('060-q')
    updater.update_graph()