import json
import os
import re

import pytest
import sqlalchemy

import server.tests.conf as st_conf
import server.model.connection as sm_connection
import server.model.match as sm_match
import server.model.schedule as sm_schedule
import server.scoutingapi as s_scout


@pytest.fixture
def scouting_app(test_event):
    assert test_event
    return s_scout.Scouting()


@pytest.fixture
def schedule():
    path = os.path.join(os.path.dirname(__file__), "test_data", "sched.json")
    with open(path) as json_file:
        json_sched = json_file.read()

    sm_schedule.process_sched(st_conf.test_event, "2017", json_sched)
    yield True
    sql = sqlalchemy.text("DELETE FROM schedules WHERE event = :evt;")
    conn = sm_connection.engine.connect()
    conn.execute(sql, evt=st_conf.test_event)
    conn.close()


def convert_to_list(text):
    return list(map(lambda item: json.loads(item),
                    re.findall("({.*})\n", text)))


# noinspection PyShadowingNames
def test_match_team_tasks(scouting_app):
    scouting_app.matchteamtask("099-q", "1983", "placeGear", "auto",
                               success=1, attempt=1)

    mt_tasks = convert_to_list(scouting_app.matchteamtasks("1983",
                                                           "099-q"))

    assert len(mt_tasks) == 1
    assert mt_tasks[0]["match"] == "099-q"
    assert mt_tasks[0]["task"] == "placeGear"
    assert mt_tasks[0]["attempts"] == 1
    assert mt_tasks[0]["successes"] == 1

