"""This module contains functions for randomly generating test data.
"""
import random

import numpy.random
import sqlalchemy

import server.model.connection as sm_connection
import server.model.dal as sm_dal
import server.model.event as sm_event
import server.model.match as sm_match
import server.model.setup as sm_setup


def create_event(rnd_event, rnd_season, base_event, base_season):
    """Creates a test event and copies a schedule from an actual event.

    To reduce risk of mixing test and actual data, season must be less
    than 2017, or function will throw assertion error.

    Args:
        rnd_event: (str) name of fictitious event that will be used for
            testing. Use a name that will not be confused with an actual
            event (e.g., include 'test' in the name)
        rnd_season: (str) Four digit year for fictitious event.
        base_event: (str) name of an event in the database that has a
            match schedule. This function will copy the base event's
            schedule to the fictitious event.
        base_season: (str) Four digit year for base event.
    """
    rnd_event_id = sm_event.EventDal.set_current_event(rnd_event, rnd_season)
    base_event_id = sm_event.EventDal.get_event_id(base_event, base_season)
    conn = sm_connection.engine.connect()

    sql = sqlalchemy.text("INSERT INTO schedules (date, event_id, level, "
                          "match, alliance, team, station) "
                          "SELECT date, :rnd_evt_id, level, match, alliance, "
                          "team, station FROM schedules "
                          "WHERE event_id = :base_evt_id;")
    conn.execute(sql, rnd_evt_id=rnd_event_id, base_evt_id=base_event_id)
    conn.close()


def get_schedule(event, season):
    """Helper function for obtainin match schedule for an event.

    Args:
        event: FIRST API event code.
        season: Four digit year specifying season.

    Returns: sqlalchemy ResultProxy object with six rows per match,
        one row per team. Key values match column names from schedules
        table.
    """
    event_id = sm_event.EventDal.get_event_id(event, season)
    conn = sm_connection.engine.connect()
    sql = sqlalchemy.text("SELECT level, match, alliance, team, station "
                          "FROM schedules WHERE event_id = :evt_id "
                          "and level = 'qual' "
                          "ORDER BY match;")
    return conn.execute(sql, evt_id=event_id)


def add_poisson_measures(event, season, task, phase, mean_attempts, acc_min,
                         acc_max, print_output=True, sql_output=False):
    assert int(season) < 2017
    sm_event.EventDal.set_current_event(event, season)
    schedule = get_schedule(event, season)
    for row in schedule:
        attempts = numpy.random.poisson(mean_attempts)
        accuracy = numpy.random.uniform(acc_min, acc_max)
        successes = round(attempts * accuracy)
        if print_output:
            print(row["team"], task, row["match"], phase, attempts, successes,
                      accuracy)
        if sql_output:
            sm_match.MatchDal.insert_match_task(row["team"], task, row["match"],
                                                phase, attempt_count=attempts,
                                                success_count=successes)


def add_start_positions(event, season):
    """Adds starting position measure for every task.

    To reduce risk of mixing test and actual data, season must be less
    than 2017, or function will throw assertion error.

    Task: startPosition
    Values 1: "Exch", 2: "Center", 3: "NonEx"

    Args:
        event: First API event name
        season: four digit season as string
    """
    assert int(season) < 2017
    sm_event.EventDal.set_current_event(event, season)
    start_positions = ["Exch", "Center", "NonEx"]
    random.shuffle(start_positions)
    schedule = get_schedule(event, season)
    idx = 1
    print("\n")  # DEBUG
    for tm_mtch in schedule:
        if idx > 3:
            idx = 1
            random.shuffle(start_positions)
        sm_match.MatchDal.insert_match_task(tm_mtch["team"], "startPosition",
                                            tm_mtch["match"], "auto",
                                            capability=start_positions[idx-1])
        idx = idx + 1


def add_enum_match_measures(event, season, task, phase, enums):
    """Adds a measure of type enum, one per match.

    Args:
        event:
        season:
        task:
        phase:
        enums:

    Returns:

    """
    assert int(season) < 2017
    sm_event.EventDal.set_current_event(event, season)
    schedule = get_schedule(event, season)

    # Obtain set of matches with no duplicates.
    matches = set([tm_mtch["match"] for tm_mtch in schedule])

    for match in matches:
        sm_match.MatchDal.insert_match_task("na", task, match, phase,
                                            capability=random.choice(enums))


def add_auto_cube_placements(event, season, scale_prob, success_prob):
    assert int(season) < 2017
    sm_event.EventDal.set_current_event(event, season)
    schedule = get_schedule(event, season)
    for tm_mtch in schedule:
        if numpy.random.binomial(1, scale_prob, 1) == 1:
            if numpy.random.binomial(1, success_prob, 1):
                sm_match.MatchDal.insert_match_task(tm_mtch["team"],
                                                    "placeScale",
                                                    tm_mtch["match"], "auto",
                                                    attempt_count=1,
                                                    success_count=1)
            else:
                sm_match.MatchDal.insert_match_task(tm_mtch["team"],
                                                    "placeScale",
                                                    tm_mtch["match"], "auto",
                                                    attempt_count=1,
                                                    success_count=0)
        else:
            if numpy.random.binomial(1, success_prob, 1):
                sm_match.MatchDal.insert_match_task(tm_mtch["team"],
                                                    "placeSwitch",
                                                    tm_mtch["match"], "auto",
                                                    attempt_count=1,
                                                    success_count=1)
            else:
                if numpy.random.binomial(1, success_prob, 1):
                    sm_match.MatchDal.insert_match_task(tm_mtch["team"],
                                                        "placeSwitch",
                                                        tm_mtch["match"],
                                                        "auto",
                                                        attempt_count=1,
                                                        success_count=0)


def test_add_measures():
    pass


def delete_test_data(event, season):
    assert int(season) < 2017
    event_id = sm_event.EventDal.get_event_id(event, season)
    sql = sqlalchemy.text("DELETE FROM measures WHERE event_id=:evt_id;")
    conn = sm_connection.engine.connect()
    conn.execute(sql, evt_id=event_id)
    sql = sqlalchemy.text("DELETE FROM schedules WHERE event_id=:evt_id;")
    conn.execute(sql, evt_id=event_id)
    sql = sqlalchemy.text("DELETE FROM events WHERE id=:evt_id;")
    conn.execute(sql, evt_id=event_id)
    conn.close()



def add_test_data():
    sm_setup.load_game_sheet("2018")
    sm_dal.rebuild_dicts()
    create_event("test_holoviews", "1318", "turing", "2017")
    sm_dal.rebuild_dicts()
    add_start_positions("test_holoviews", "1318")
    add_enum_match_measures("test_holoviews", "1318", "assignColors", "auto",
                             ["RBR", "BRB", "RRR", "BBB"])
    add_auto_cube_placements("test_holoviews", "1318", 0.2, 0.3)
    add_poisson_measures("test_holoviews", "1318", "placeSwitch", "teleop", 7,
                         0.5, 1,
                         sql_output=True)
    add_poisson_measures("test_holoviews", "1318", "placeScale", "teleop", 4,
                         0.1, 0.7, sql_output=True)
