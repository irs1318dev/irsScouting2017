import csv
import os
import db
import db_dimensiondata as ddd
import firstapi as api
import json
from sqlalchemy.sql import text
import db_dimensiondata as data
import scouting.match as m
import scouting.event as e


def load_game_sheet():
    fpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(fpath)
    file = open('gametasks.csv')
    sheet = csv.reader(file)

    ddd.add_many_cols("task_options", {'task_name': 'na',
                                       'type': 'capability',
                                       'option_name': 'na'})
    for row in sheet:
        if row[0] != 'actor':
            insert_game(row[0], row[1], row[2], row[3], row[4], row[5], row[8])


def insert_game(actor, task, claim, auto, teleop, finish, optionString):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO games (actor, task, claim, auto, teleop, finish) "
        "VALUES (:actor,:task,:claim,:auto,:teleop,:finish) "
        "ON CONFLICT (task) "
        "DO UPDATE "
        "SET actor=:actor, task=:task, claim=:claim, auto=:auto, teleop=:teleop, finish=:finish;")
    conn.execute(select, actor=actor, task=task, claim=claim, auto=auto, teleop=teleop, finish=finish)
    data.add_name("tasks", "name", task)

    if not optionString.strip():
        optionNames = optionString.split('|')
        for optionName in optionNames:
            ddd.add_many_cols("task_options", {'task_name': task,
                                           'type': 'capability',
                                           'option_name': optionName})


def insert_sched(event, season, level='qual'):
    engine = db.getdbengine()
    conn = engine.connect()
    event = event.lower()
    sched_json = api.getSched(event.upper(), season, level)
    sched = json.loads(sched_json)['Schedule']

    select = text(
        "INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
        "VALUES (:event,'na','na','na','na','na','na'); "
    )
    conn.execute(select, event=event)

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


def insert_MatchResults(event, season, tournamentLevel):
    event = event.lower()
    score_json = api.getMatchScores(event, season, tournamentLevel)
    matchScores = json.loads(score_json)['MatchScores']
    for mch in matchScores:
        matchNumber = mch['matchNumber']
        match = "{0:0>3}-q".format(matchNumber)
        for alnce in mch['Alliances']:
            load_robot_movebaseline(event, match, alnce, 1)
            load_robot_movebaseline(event, match, alnce, 2)
            load_robot_movebaseline(event, match, alnce, 3)
            # load_alliance_measure(event, match, alnce, 'autoFuelLow')
            # load_alliance_measure(event, match, alnce, 'autoFuelHigh')
            # load_alliance_measure(event, match, alnce, 'teleopFuelLow')
            # load_alliance_measure(event, match, alnce, 'teleopFuelHigh')
            # load_alliance_measure(event, match, alnce, 'foulCount')
            # load_alliance_measure(event, match, alnce, 'techFoulCount')
            # load_alliance_measure(event, match, alnce, 'autoPoints')
            # load_alliance_measure(event, match, alnce, 'autoMobilityPoints')
            # load_alliance_measure(event, match, alnce, 'autoRotorPoints')
            # load_alliance_measure(event, match, alnce, 'teleopPoints')
            # load_alliance_measure(event, match, alnce, 'teleopFuelPoints')
            # load_alliance_measure(event, match, alnce, 'teleopRotorPoints')
            # load_alliance_measure(event, match, alnce, 'teleopTakeoffPoints')
            # load_alliance_measure(event, match, alnce, 'kPaBounsPoints')
            # load_alliance_measure(event, match, alnce, 'rotorBonusPoints')
            # load_alliance_measure(event, match, alnce, 'adjustPoints')
            # load_alliance_measure(event, match, alnce, 'foulPoints')

            # load_alliance_measure(event, match, alnce, 'totalPoints','finalScore', 'final')

def load_robot_movebaseline(event, match, alnce, station):
    robotKey = 'robot' + str(station) + 'Auto'
    robot1Auto = alnce[robotKey]
    alliance = alnce['alliance'].lower()
    match_details = e.EventDal.match_details_station(event, match, alliance, str(station))
    team1 = match_details['team']
    success_count = 0
    attempt_count = 1
    if robot1Auto == 'Mobility':
        success_count = 1
    m.MatchDal.matchteamtask(team1, "moveBaseline", match, "auto", 0, attempt_count, success_count)


def load_alliance_measure(event, match, alnce, firstApiTaskName, taskName, phase):
    Value = alnce[firstApiTaskName]
    alliance = alnce['alliance'].lower()
    success_count = Value
    attempt_count = Value #to do have matchteamtask accept allaince
    m.MatchDal.matchteamtask('na', taskName, match, phase, 0, attempt_count, success_count)
