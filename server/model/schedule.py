import json
import os
import pandas
import sqlalchemy

from sqlalchemy import text

import server.model.event as sm_event
import server.model.firstapi as api
import server.model.connection as smc
import server.model.upsert as smu
import server.model.firstapi as smf


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


def set_teams():
    conn = smc.engine.connect()
    sql = text("SELECT name FROM teams;")
    teams = conn.execute(sql).fetchall()
    teams = [tm[0] for tm in teams]
    # sql = text("UPDATE teams SET long_name = :long_name WHERE name = :name;")
    # names = json.loads(smf.get_team_names(teams[13][0]))
    # conn.execute(sql, long_name=names["teams"][0]["nameShort"], name=teams[13][0])
    for name in teams:

        try:
            names = json.loads(smf.get_team_names(name))
            sql = text("UPDATE teams SET long_name = :long_name WHERE name = :name;").bindparams(
                long_name=names["teams"][0]["nameShort"], name=name)
            conn.execute(sql)
        except:
            print("Error setting team")


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
    set_teams() 


# Function only works if the csv has columns in the order of match, red1, red2, red3, blue1, blue2, blue3
def manual_Entry(file, event, season):
    data = pandas.read_csv(file)
    match = list(data.iloc[:, 0])
    red1 = list(data.iloc[:, 1])
    red2 = list(data.iloc[:, 2])
    red3 = list(data.iloc[:, 3])
    blue1 = list(data.iloc[:, 4])
    blue2 = list(data.iloc[:, 5])
    blue3 = list(data.iloc[:, 6])
    event_id = sm_event.EventDal.get_event_id(event, season)
    value = 0
    conn = smc.engine.connect()
    for elem in match:
        r1 = int(red1[value])
        r2 = int(red2[value])
        r3 = int(red3[value])
        elem = int(elem)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :r1, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, r1=r1, event_id=event_id)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :r2, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, r2=r2, event_id=event_id)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :r3, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, r3=r3, event_id=event_id)
        value = value + 1
    value = 0
    for elem in match:
        b1 = int(blue1[value])
        b2 = int(blue2[value])
        b3 = int(blue3[value])
        elem = int(elem)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :b1, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, b1=b1, event_id=event_id)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :b2, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, b2=b2, event_id=event_id)
        select = sqlalchemy.text("INSERT INTO schedules (match, team, level, date, alliance, station, event_id) " +
                                 "VALUES (:elem, :b3, 'na', 'na', 'red', 'na', :event_id);")
        conn.execute(select, elem=elem, b3=b3, event_id=event_id)
        value = value + 1
    conn.close()
