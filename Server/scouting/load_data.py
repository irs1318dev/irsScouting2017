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
            insertgame(row[0],row[1],row[2],row[3],row[4],row[5])


def insertgame(actor, task, claim, auto, teleop, finish):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO games (actor, task, claim, auto, teleop, finish) " +
        "VALUES (:actor,:task,:claim,:auto,:teleop,:finish); "
    )
    conn.execute(select, actor=actor, task=task, claim=claim, auto=auto, teleop=teleop, finish=finish)


def insertsched(event, season, level='qual'):
    engine = db.getdbengine()
    conn = engine.connect()
    sched_json = api.getSched(event, season, level)
    sched = json.loads(sched_json)['Schedule']
    for mch in sched:
        match = mch['matchNumber']
        date = mch['startTime']
        for tm in mch['Teams']:
            team = tm['teamNumber']
            station = tm['station']
            alliance = tm['station'][0:-1]
            select = text(
                "INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
                "VALUES (:event,:match,:team,:level,:date,:alliance,:station); "

            )
            conn.execute(select, event=event, match=match, team=team, level=level, date=date, alliance=alliance, station=station)




