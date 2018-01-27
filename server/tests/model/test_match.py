import json
import re

import pytest

import server.scouting.event
import server.model.match as smm


@pytest.fixture
def event(restored_testdb):
    assert restored_testdb
    server.scouting.event.EventDal.set_current_event("turing")
    return server.scouting.event.EventDal.get_current_event()


def match(restored_testdb):
    assert restored_testdb
    server.scouting.event.EventDal.set_current_match("001-q")
    return server.scouting.event.EventDal.get_current_match()


def test_build_dicts(event):
    assert event == "turing"
    # Dates
    dates, date_ids = smm.build_dicts("dates")
    assert len(dates) == 1029
    assert isinstance(dates["2017-03-04T16:12:00"], int)
    assert len(date_ids) == 1029
    assert "2017-03-04T17:36:00" in date_ids.values()

    # Levels
    levels, level_ids = smm.build_dicts("levels")
    assert isinstance(levels["playoff"], int)
    assert "qual" in level_ids.values()
    assert len(levels) == 3

    # WARNING: GAME DEPENDENT
    # Task Options
    tasks_options, task_option_ids = smm.build_dicts("task_options")
    assert len(task_option_ids) == 103
    assert len(tasks_options) == 103
    assert "startingLocation-boiler" in task_option_ids.values()
    assert isinstance(tasks_options["robotTechFoul-"], int)


def test_match_teams(event):
    assert event
    matches = re.split("\n", smm.MatchDal.match_teams("001-q"))
    # Verify JSON strings have correct format.
    for alliance in matches[0:2]:
        ptn = (r'{"alliance":"(red|blue)", "match":"\d{3}-(p|q)", '
            r'"team1":"\d{1,4}", "team2":"\d{1,4}", "team3":"\d{1,4}"}')
        assert re.match(ptn, alliance)
    # Verify function returns both a red and blue alliance.
    assert (json.loads(matches[0])["alliance"] !=
           json.loads(matches[1])["alliance"])


def test_pit_teams(event):
    assert event
    pit_teams = smm.MatchDal.pit_teams()
    ptn = r'{"match":"na", "teams":\["\d{1,4}"(,"\d{1,4}")*,"na"\]}'
    assert re.match(ptn, pit_teams)


def test_match_team_tasks(event):
    assert event
    mt_tasks = re.split("\n", smm.MatchDal.match_team_tasks("001-q", "1983"))
    assert len(mt_tasks) == 7
    ptn = (r'{"match": "001-q", "team": "1983", "task": "placeGear", '
           '"phase": "auto", "actor": "robot", "measuretype": "boolean", '
           '"capability": 0, "attempts": 1, "successes": 0, "cycle_times": 0}')
    assert re.match(ptn, mt_tasks[0])


def test_match_team_task(restored_testdb):
    pass





