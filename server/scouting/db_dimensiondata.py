from server.model.update import upsert, upsert_range


def insert_data():
    upsert("levels", "name", "na")
    upsert("levels", "name", "qual")
    upsert("levels", "name", "playoff")

    upsert_range("matches", "name", 150, "{0:0>3}-q")
    upsert("matches", "name", "na")
    upsert("matches", "name", "q1.1")
    upsert("matches", "name", "q1.2")
    upsert("matches", "name", "q1.3")
    upsert("matches", "name", "q2.1")
    upsert("matches", "name", "q2.2")
    upsert("matches", "name", "q2.3")
    upsert("matches", "name", "q3.1")
    upsert("matches", "name", "q3.2")
    upsert("matches", "name", "q3.3")
    upsert("matches", "name", "s1.1")
    upsert("matches", "name", "s1.2")
    upsert("matches", "name", "s1.3")
    upsert("matches", "name", "s2.1")
    upsert("matches", "name", "s2.2")
    upsert("matches", "name", "s2.3")
    upsert("matches", "name", "f1")
    upsert("matches", "name", "f2")
    upsert("matches", "name", "f3")

    upsert("alliances", "name", "na")
    upsert("alliances", "name", "blue")
    upsert("alliances", "name", "red")

    upsert("dates", "name", "na")

    # teams imported from schedule
    upsert("teams", "name", 'na')



    upsert("stations", "name", "na")
    upsert("stations", "name", "1")
    upsert("stations", "name", "2")
    upsert("stations", "name", "3")


    upsert("actors", "name", "na")
    upsert("actors", "name", "drive_team")
    upsert("actors", "name", "robot")
    upsert("actors", "name", "pilot")
    upsert("actors", "name", "human_player")
    upsert("actors", "name", "alliance")
    upsert("actors", "name", "team")

    # tasks imported from game
    upsert("tasks", "name", 'na')

    upsert("measuretypes", "name", "na")
    upsert("measuretypes", "name", "count")
    upsert("measuretypes", "name", "percentage")
    upsert("measuretypes", "name", "boolean")
    upsert("measuretypes", "name", "enum")
    upsert("measuretypes", "name", "attempt")
    upsert("measuretypes", "name", "cycletime")

    upsert("phases", "name", "na")
    upsert("phases", "name", "claim")
    upsert("phases", "name", "auto")
    upsert("phases", "name", "teleop")
    upsert("phases", "name", "finish")

    upsert("attempts", "name", "summary")
    upsert_range("attempts", "name", 31, "{0:0>2}")

    upsert("reasons", "name", "na")
    upsert("reasons", "name", "dropped")
    upsert("reasons", "name", "blocked")
    upsert("reasons", "name", "defended")







