"""This module contains functions for randomly generating test data.
"""
import random

import numpy.random
import sqlalchemy

import server.model.connection as sm_connection
import server.model.dal as sm_dal
import server.model.match as sm_match


def create_event(rnd_event, base_event):
    """
    Args:
        rnd_event: (str) name of fictitious event that will be used for
            testing. Use a name that will not be confused with an actual
            event (e.g., include 'test' in the name)
        base_event: (str) name of an event in the database that has a
            match schedule. This function will copy the base event's
            schedule to the fictitious event.
    """
    conn = sm_connection.engine.connect()

    sql = sqlalchemy.text("INSERT INTO schedules (date, event, level, match, "
                          "alliance, team, station) "
                          "SELECT date, :rnd_evt, level, match, alliance, team,"
                          "station FROM schedules "
                          "WHERE event = :base_evt;")
    conn.execute(sql, rnd_evt=rnd_event, base_evt=base_event)


    sql = sqlalchemy.text("INSERT INTO events (name, state, type, season) "
                          "VALUES (:rnd_evt, 'XX', 'TEST', '2018');")
    conn.execute(sql, rnd_evt=rnd_event)
    conn.close()


# create_event("test_holoviews", "turing")


def add_poisson_measures(event, task, phase, mean_attempts, acc_min, acc_max,
                         print_output=True, sql_output=False):
    conn = sm_connection.engine.connect()
    sql = sqlalchemy.text("SELECT level, match, alliance, team, station "
                          "FROM schedules WHERE event = :evt "
                          "and level = 'qual';")
    results = conn.execute(sql, evt=event)
    for row in results:
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


def test_add_measures():
    add_poisson_measures("test_holoviews", "placeSwitch", "teleop", 7, 0.5, 1,
                         sql_output=True)