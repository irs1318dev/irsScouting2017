import csv
import os
import scouting.db as db
import scouting.db_dimensiondata as ddd
import firstapi as api
import json
from sqlalchemy.sql import text
import scouting.db_dimensiondata as data
import scouting.match as m
import scouting.event as e


engine = db.getdbengine()


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
    select = text(
        "INSERT INTO games (actor, task, claim, auto, teleop, finish) "
        "VALUES (:actor,:task,:claim,:auto,:teleop,:finish) "
        "ON CONFLICT (task) "
        "DO UPDATE "
        "SET actor=:actor, task=:task, claim=:claim, auto=:auto, teleop=:teleop, finish=:finish;")
    conn = engine.connect()
    conn.execute(select, actor=actor, task=task, claim=claim, auto=auto, teleop=teleop, finish=finish)
    conn.close()
    data.add_name("tasks", "name", task)

    if not optionString.strip():
        optionNames = optionString.split('|')
        for optionName in optionNames:
            ddd.add_many_cols("task_options", {'task_name': task,
                                           'type': 'capability',
                                           'option_name': optionName})


def insert_sched(event, season, level='qual', fileName = '-1'):
    event = event.lower()

    if fileName == '-1':
        sched_json = api.getSched(event.upper(), season, level)
    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        sched_json = open(fileName).read()

    process_sched(event, season, sched_json, level)


def process_sched(event, season, sched_json, level='qual'):
    sched = json.loads(sched_json)['Schedule']

    select = text(
        "INSERT INTO schedules (event, match, team, level, date, alliance, station) " +
        "VALUES (:event,'na','na','na','na','na','na'); "
    )
    conn = engine.connect()
    conn.execute(select, event=event)
    conn.close()

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
            conn = engine.connect()
            conn.execute(select, event=event, match=match, team=team, level=level, date=date, alliance=alliance,
                         station=station)
            conn.close()
            data.add_name("events", "name", event)
            data.add_name("teams", "name", team)
            data.add_name("dates", "name", date)


def insert_all_events(season, tournamentLevel, fileName = '-1'):
    if fileName == '-1':
        event_json = api.getEvents(season, tournamentLevel)

    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        event_json = open(fileName).read()

    process_all_events(season, event_json, tournamentLevel)


def process_all_events(season, event_json, tournamentLevel):
    eve = json.loads(event_json)['Events']
    initial_event = e.EventDal.get_current_event()
    print('Initial event is ' + initial_event)
    for event in eve:
        loading_event = event['code']
        print('Setting current event to ' + loading_event)
        e.EventDal.set_current_event(loading_event)
        print("insert sched for " + loading_event)
        insert_sched(event['code'], season, tournamentLevel)
    for event in eve:
        loading_event = event['code']
        print('Setting current event to ' + loading_event)
        print("load match results for " + loading_event)
        insert_MatchResults(loading_event, season, tournamentLevel)

    print('Resetting current event to ' + initial_event)
    e.EventDal.set_current_event(initial_event)



def insert_MatchResults(event, season, tournamentLevel, fileName = '-1'):
    event = event.lower()
    if fileName == '-1':
        score_json = api.getMatchScores(event, season, tournamentLevel)

    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        score_json = open(fileName).read()
        process_match_results(event, season, tournamentLevel, score_json)

    process_match_results(event, season, tournamentLevel, score_json)


def process_match_results(event, season, tournamentLevel, score_json):
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
            load_alliance_measure(event, match, alnce, 'totalPoints', 'totalPoints', 'finish')

            load_alliance_flag(event, match, alnce, 'rotor1Auto', 'rotor1Auto', 'auto')
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
