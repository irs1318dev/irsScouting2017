import json
import os

from sqlalchemy import text

import server.model.event as sm_event
import server.model.firstapi as api
import server.model.connection as smc
import server.model.upsert as smu


def insert_sched(event, season, level='qual', fileName = '-1'):
    event = event.lower()

    if fileName == '-1':
        sched_json = api.schedule(event.upper(), season, level)
    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        sched_json = open(fileName).read()

    process_sched(event, season, sched_json, level)


def process_sched(event, season, sched_json, level='qual'):
    sched = json.loads(sched_json)['Schedule']
    smu.upsert_cols("events", {"name": event, "season": season})
    event_id = sm_event.EventDal.get_event_id(event, season)

    select = text(
        "INSERT INTO schedules (event_id, match, team, level, date, "
        "alliance, station) " +
        "VALUES (:evt_id,'na','na','na','na','na','na'); "
    )
    conn = smc.engine.connect()
    conn.execute(select, evt_id=event_id)
    conn.close()

    for mch in sched:
        match = "{0:0>3}-q".format(mch['matchNumber'])
        date = mch['startTime']
        for tm in mch['teams']:
            team = tm['teamNumber']
            station = tm['station'][-1:]
            alliance = tm['station'][0:-1].lower()
            select = text(
                "INSERT INTO schedules (event_id, match, team, level, "
                "date, alliance, station) " +
                "VALUES (:evt_id,:match,:team,:level,:date,:alliance,:station);"
            )
            conn = smc.engine.connect()
            conn.execute(select, evt_id=event_id, match=match, team=team,
                         level=level, date=date, alliance=alliance,
                         station=station)
            conn.close()
            # smu.upsert("events", "name", event)
            smu.upsert("teams", "name", team)
            smu.upsert("dates", "name", date)