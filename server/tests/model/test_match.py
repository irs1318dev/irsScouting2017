import json
import re

import server.model.match as smm


def test_build_dicts():
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


def test_match_teams():
    matches = re.split("\n", smm.MatchDal.match_teams("001-q"))
    # Verify JSON strings have correct format.
    for alliance in matches[0:2]:
        ptn = (r'{"alliance":"(red|blue)", "match":"\d{3}-(p|q)", '
            r'"team1":"\d{1,4}", "team2":"\d{1,4}", "team3":"\d{1,4}"}')
        assert re.match(ptn, alliance)
    # Verify function returns both a red and blue alliance.
    assert (json.loads(matches[0])["alliance"] !=
           json.loads(matches[1])["alliance"])


def test_pit_teams():
    pit_teams = smm.MatchDal.pit_teams()
    ptn = r'{"match":"na", "teams":\["\d{1,4}"(,"\d{1,4}")*,"na"\]}'
    assert re.match(ptn, pit_teams)


