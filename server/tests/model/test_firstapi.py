import json

import server.auth
import server.model.firstapi


def test_schedule():
    sched = json.loads(server.model.firstapi.schedule("pncmp", "2017"))
    assert sched["Schedule"][0]["teams"][0]["teamNumber"] == 2910
    assert len(sched["Schedule"]) == 128
#
#
# def test_match_results():
#     match_res = json.loads(
#         server.model.firstapi.match_results("pncmp", "2017", 1))
#     assert match_res["Matches"][0]["scoreBlueFinal"] == 285
#
#
# def test_match_scores():
#     scores = json.loads(server.model.firstapi.match_scores(
#         "pncmp", "2017"))
#     assert len(scores["MatchScores"]) == 128
#     assert scores["MatchScores"][0]["alliances"][0]["teleopPoints"] == 270
