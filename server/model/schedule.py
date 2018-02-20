import json
import os
import pandas
import sqlalchemy

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


# Function only works if the csv has columns in the order of match, red1, red2, red3, blue1, blue2, blue3
def manual_Entry(file):
    data = pandas.read_csv(file)
    match = data.iloc[:, 0]
    match = list(match)
    red1 = data.iloc[:, 1]
    red1 = list(red1)
    red2 = data.iloc[:, 2]
    red2 = list(red2)
    red3 = data.iloc[:, 3]
    red3 = list(red3)
    blue1 = data.iloc[:, 4]
    blue1 = list(blue1)
    blue2 = data.iloc[:, 5]
    blue2 = list(blue2)
    blue3 = data.iloc[:, 6]
    blue3 = list(blue3)
    value = 0
    conn = smc.engine.connect()
    for elem in match:
        r1 = int(red1[value])
        r2 = int(red2[value])
        r3 = int(red3[value])
        elem = int(elem)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :r1, 'na', 'na', 'red', 'na');")
        conn.execute(select, elem=elem, r1=r1)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :r2, 'na', 'na', 'red', 'na');")
        conn.execute(select, elem=elem, r2=r2)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :r3, 'na', 'na', 'red', 'na');")
        conn.execute(select, elem=elem, r3=r3)
        value = value + 1
    value = 0
    for elem in match:
        b1 = int(blue1[value])
        b2 = int(blue2[value])
        b3 = int(blue3[value])
        elem = int(elem)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :b1, 'na', 'na', 'blue', 'na');")
        conn.execute(select, elem = elem, b1=b1)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :b2, 'na', 'na', 'blue', 'na');")
        conn.execute(select, elem = elem, b2=b2)
        select = sqlalchemy.text("INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                                 "VALUES ('na', :elem, :b3, 'na', 'na', 'blue', 'na');")
        conn.execute(select, elem = elem, b3=b3)
        value = value + 1
    conn.close()

