"""This module contains functions for randomly generating test data.
"""
import sqlalchemy

import server.model.connection as sm_connection

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


create_event("test_holoviews", "turing")