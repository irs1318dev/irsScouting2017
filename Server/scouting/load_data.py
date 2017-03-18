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
            load_alliance_measure(event, match, alnce, 'autoFuelLow', 'autoFuelLow', 'finish')
            load_alliance_measure(event, match, alnce, 'autoFuelHigh', 'autoFuelHigh', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopFuelLow', 'teleopFuelHigh', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopFuelHigh', 'teleopFuelHigh', 'finish')
            load_alliance_measure(event, match, alnce, 'foulCount', 'foulCount', 'finish')
            load_alliance_measure(event, match, alnce, 'techFoulCount', 'techFoulCount', 'finish')
            load_alliance_measure(event, match, alnce, 'autoPoints', 'autoPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'autoMobilityPoints', 'autoMobilityPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'autoRotorPoints', 'autoRotorPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopPoints', 'teleopPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopFuelPoints', 'teleopFuelPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopRotorPoints', 'teleopRotorPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'teleopTakeoffPoints', 'teleopTakeoffPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'kPaBonusPoints', 'kPaBonusPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'rotorBonusPoints', 'rotorBonusPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'adjustPoints', 'adjustPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'foulPoints', 'foulPoints', 'finish')
            load_alliance_measure(event, match, alnce, 'totalPoints','totalPoints', 'finish')

            load_alliance_flag(event, match, alnce, 'rotor1Auto','rotor1Auto', 'auto')
            load_alliance_flag(event, match, alnce, 'rotor2Auto', 'rotor2Auto', 'auto')
            load_alliance_flag(event, match, alnce, 'rotor1Engaged', 'rotor1Engaged', 'finish')
            load_alliance_flag(event, match, alnce, 'rotor2Engaged', 'rotor2Engaged', 'finish')
            load_alliance_flag(event, match, alnce, 'rotor3Engaged', 'rotor3Engaged', 'finish')
            load_alliance_flag(event, match, alnce, 'rotor4Engaged', 'rotor4Engaged', 'finish')
            load_alliance_flag(event, match, alnce, 'kPaRankingPointAchieved', 'kPaRankingPointAchieved', 'finish')
            load_alliance_flag(event, match, alnce, 'rotorRankingPointAchieved', 'rotorRankingPointAchieved', 'finish')
            load_alliance_flag(event, match, alnce, 'touchpadNear', 'touchpadNear', 'finish')
            load_alliance_flag(event, match, alnce, 'touchpadMiddle', 'touchpadMiddle', 'finish')
            load_alliance_rotors(event, match, alnce, 'rotorCount', 'finish')


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


def load_alliance_rotors(event, match, alnce, task, phase):
    alliance = alnce['alliance'].lower()
    r1 = alnce['rotor1Engaged']
    r2 = alnce['rotor2Engaged']
    r3 = alnce['rotor3Engaged']
    r4 = alnce['rotor4Engaged']
    attempt_count = 4
    success_count = 0
    if r4:
        success_count = 4
    elif r3:
        success_count = 3
    elif r2:
        success_count = 2
    elif r1:
        success_count = 1

    m.MatchDal.matchalliancetask(alliance, task, phase, match, 0, attempt_count, success_count, 0)


def load_alliance_flag(event, match, alnce, firstApiTaskName, taskName, phase):
    Value = alnce[firstApiTaskName]
    alliance = alnce['alliance'].lower()
    success_count = 0
    attempt_count = 1
    if Value:
        success_count = 1
    m.MatchDal.matchalliancetask(alliance, taskName, phase, match, 0, attempt_count, success_count)


def load_alliance_measure(event, match, alnce, firstApiTaskName, taskName, phase):
    Value = alnce[firstApiTaskName]
    alliance = alnce['alliance'].lower()
    success_count = Value
    attempt_count = Value
    m.MatchDal.matchalliancetask(alliance, taskName, phase, match, 0, attempt_count, success_count)
