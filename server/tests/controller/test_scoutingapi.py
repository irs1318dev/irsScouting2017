import json
import pytest
import re

import server.model.event as sm_event
import server.scoutingapi as s_scout


current_event = "turing"
current_match = "001-q"


@pytest.fixture
def event_match():
    sm_event.EventDal.set_current_event("turing", "2017")
    sm_event.EventDal.set_current_match("001-q")
    return True


@pytest.fixture()
def scouting_app(event_match):
    assert event_match
    return s_scout.Scouting()


def check_title(title, html):
    ptn = r"<title>" + title + r"</title>"
    assert re.search(ptn, html) is not None


def check_css(html):
    ptn = (r'<link rel="stylesheet" type="text/css" ' 
           r'href="web/scripts/styles.css">')
    assert re.search(ptn, html) is not None


def check_javascript(html, script):
    ptn = (r'<script type="text/javascript" '
           r'src="web/scripts/' + script + '"></script>')
    assert re.search(ptn, html) is not None


def check_tag(tag, content, html):
    ptn = r'<' + tag.lower() + r'>' + content + r'</' + tag.lower() + r'>'
    print(ptn)
    assert re.search(ptn, html) is not None


def check_header(title, script, html):
    check_title(title, html)
    check_css(html)
    check_javascript(html, script)


def convert_to_list(text):
    return list(map(lambda item: json.loads(item),
                    re.findall("({.*})\n", text)))


def check_keys(test_results, keys):
    assert len(set(keys) - set(test_results)) == 0


def test_index(scouting_app):
    html = scouting_app.index()
    check_header("IRS Scouting Director", "tablets.js", html)
    ptn = r'<h3 class = "title">Current Event: ' + current_event + r'</h3>'
    assert re.search(ptn, html) is not None
    ptn = r'<h3 class = "title">Current Match: ' + current_match + '</h3>'
    assert re.search(ptn, html) is not None
    check_tag("h1", "IRS Scouting Director", html)


def test_setup(scouting_app):
    html = scouting_app.setup()
    check_header("IRS Scouting Director", "setup.js", html)
    check_tag("h1", "IRS Server Maintanance and setup", html)
    tag = (r'<input type="text" id="event" name="Event Number" value="' +
           current_event + '"/>')
    assert re.search(tag, html) is not None
    check_tag("h3",
              '<a href="/web/sites/directions.html">Server Directions</a>',
              html)


def test_game_layout(scouting_app):
    layout = convert_to_list(scouting_app.gamelayout())
    check_keys(layout[0].keys(), ["actor", "category", "newpart", "observer",
                                  "phase", "position", "tasks"])


def test_gametasks(scouting_app):
    tasks = convert_to_list(scouting_app.gametasks())
    check_keys(tasks[0].keys(), ["actor", "auto", "claim", "enums", "finish",
                                 "miss", "success", "task", "teleop"])


def test_matches(scouting_app):
    matches = json.loads(scouting_app.matches())
    assert isinstance(matches, list)
    assert len(matches) == 113
    assert matches[0]["match"] == "001-q"
    assert matches[0]["event"] == "turing"


def test_matchteams(scouting_app):
    match_teams = convert_to_list(scouting_app.matchteams())
    assert match_teams[0]["alliance"] == "red"
    assert match_teams[1]["alliance"] == "blue"
    assert match_teams[0]["match"] == "001-q"
    assert match_teams[1]["team3"] == "1540"

    pit_teams = json.loads(scouting_app.matchteams("na"))
    assert isinstance(pit_teams, dict)
    assert pit_teams["match"] == "na"
    assert len(pit_teams["teams"]) == 68
    assert pit_teams["teams"][2] == "1287"

    match_teams2 = convert_to_list(scouting_app.matchteams("099-q"))
    assert match_teams2[0]["alliance"] == "red"
    assert match_teams2[1]["alliance"] == "blue"
    assert match_teams2[0]["match"] == "099-q"
    assert match_teams2[1]["team3"] == "6384"


def test_matchteamtasks(scouting_app):
    team_tasks = convert_to_list(scouting_app.matchteamtasks("1318",
                                                             "007-q"))
    assert len(team_tasks) == 10
    assert team_tasks[0]["match"] == "007-q"
    assert team_tasks[8]["task"] == "pushTouchPad"
    print("\n", team_tasks)
