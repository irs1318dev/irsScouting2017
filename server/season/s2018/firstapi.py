import json

import pandas

import server.model.event as sm_event
import server.model.firstapi as sm_firstapi


def download_platform_color():
    _, event_name, event_season = sm_event.EventDal.get_current_event()
    raw_scores = sm_firstapi.match_scores(event_name, event_season)
    scores = json.loads(raw_scores)

    match_levels = [mtch["matchLevel"] for mtch in scores["MatchScores"]]
    match_numbers = [mtch["matchNumber"] for mtch in scores["MatchScores"]]
    switchLeftNearColors = [mtch["switchLeftNearColor"][0] for mtch in
                            scores["MatchScores"]]
    scaleNearColors = [mtch["scaleNearColor"][0] for mtch in
                       scores["MatchScores"]]
    switchRightNearColors = [mtch["switchRightNearColor"][0] for mtch in
                             scores["MatchScores"]]

    colors = []
    for idx in range(len(scaleNearColors)):
        colors.append(switchLeftNearColors[idx] + scaleNearColors[idx] +
                      switchRightNearColors[idx])

    colors_df = pandas.DataFrame({"matches": match_numbers,
                                  "level": match_levels,
                                  "platform_colors": colors})
    for mtch in colors_df.itertuples():
        pass