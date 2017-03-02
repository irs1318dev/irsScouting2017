import csv
import os
import db
import firstapi as api
import json
from sqlalchemy.sql import text
import db_dimensiondata as data


def loadGameSheet():
    fpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(fpath)
    file = open('gametasks.csv')
    sheet = csv.reader(file)
    for row in sheet:
        if row[0] != 'actor':
            insertgame(row[0], row[1], row[2], row[3], row[4], row[5], row[8])


def insertgame(actor, task, claim, auto, teleop, finish, optionString):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO games (actor, task, claim, auto, teleop, finish) " +
        "VALUES (:actor,:task,:claim,:auto,:teleop,:finish); "
    )
    conn.execute(select, actor=actor, task=task, claim=claim, auto=auto, teleop=teleop, finish=finish)
    data.add_name("tasks", "name", task)
    # create task options if enums is filled with a non-empty value
    # split on | a dn insert one record for each task, 'capabliity', optionName.


def insertsched(event, season, level='qual'):
    engine = db.getdbengine()
    conn = engine.connect()
    event = event.lower()
    sched_json = api.getSched(event.upper(), season, level)
    sched = json.loads(sched_json)['Schedule']
    for mch in sched:
        match = "{0:0>3}-q".format(mch['matchNumber'])
        date = mch['startTime']
        for tm in mch['Teams']:
            team = tm['teamNumber']
            station = tm['station'][-1:]
            alliance = tm['station'][0:-1].lower()
            select = text(
                "INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                "VALUES (:event,:match,:team,:level,:date,:alliance,:station); "

            )
            conn.execute(select, event=event, match=match, team=team, level=level, date=date, alliance=alliance, station=station)
            data.add_name("events", "name", event)
            data.add_name("teams", "name", team)
            data.add_name("dates", "name", date)








