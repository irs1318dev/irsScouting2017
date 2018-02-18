import os.path
import pytest
import re
import sqlalchemy

import server.model.connection as sm_connection
import server.model.dal as sm_dal
import server.model.event as sm_event
import server.model.match as sm_match
import server.model.schedule as sm_schedule
import server.tests.conf as st_conf


@pytest.fixture
def schedule():
    path = os.path.join(os.path.dirname(__file__), "test_data", "sched.json")
    with open(path) as json_file:
        json_sched = json_file.read()

    sm_schedule.process_sched(st_conf.test_event[0],
                              st_conf.test_event[1], json_sched)
    yield True
    sql = sqlalchemy.text("DELETE FROM schedules "
                          "WHERE event_id = :evt_id;")
    conn = sm_connection.engine.connect()
    event_id = sm_event.EventDal.get_event_id(st_conf.test_event[0],
                                              st_conf.test_event[1])
    conn.execute(sql, evt_id=event_id)
    conn.close()


# noinspection PyShadowingNames
def test_match_team_task(test_event):
    assert test_event
    sm_match.MatchDal.insert_match_task("1983", "placeGear", "001-q",
                                        "auto", attempt_count=1)
    mt_tasks = re.split("\n", sm_match.MatchDal.match_team_tasks("001-q",
                                                                 "1983"))
    mt_tasks = [val for val in mt_tasks if val != '']
    # assert len(mt_tasks) == 1
    print(mt_tasks)
    ptn = (r'{"match": "001-q", "team": "1983", "task": "placeGear", '
           '"phase": "auto", "actor": "robot", "measuretype": "boolean", '
           '"capability": 0, "attempts": 1, "successes": 0, "cycle_times": 0}')
    assert re.match(ptn, mt_tasks[0])


# noinspection PyShadowingNames
def test_alliance_task(test_event, schedule):
    assert test_event
    assert schedule
    sm_match.MatchDal.insert_alliance_task("blue", "moveBaseline", "claim",
                                           "001-q", capability=1)
    sql = sqlalchemy.text("SELECT * FROM measures "
                          "WHERE match_id = :mtch AND alliance_id = :alli "
                          "AND phase_id = :phs AND event_id = :evt;")
    match_id = sm_dal.match_ids["001-q"]
    alliance_id = sm_dal.alliance_ids["blue"]
    phase_id = sm_dal.phase_ids["claim"]
    task_id = sm_dal.task_ids["moveBaseline"]
    event_id = sm_event.EventDal.get_event_id(st_conf.test_event[0],
                                              st_conf.test_event[1])
    conn = sm_connection.engine.connect()
    results = conn.execute(sql, mtch=match_id, alli=alliance_id, phs=phase_id,
                           evt=event_id)
    assert results.rowcount == 1
    row = results.fetchone()
    assert row["match_id"] == match_id
    assert row["alliance_id"] == alliance_id
    assert row["task_id"] == task_id
    results.close()
