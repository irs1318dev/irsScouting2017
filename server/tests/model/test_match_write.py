import re

import server.model.match as sm_match
import server.tests.conf as st_conf


# noinspection PyShadowingNames
def test_match_team_task(test_event):
    assert test_event["event"] == st_conf.test_event
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






