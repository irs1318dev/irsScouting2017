import os

import server.model.connection
import server.model.upsert
import server.model.firstapi as api
import json
import server.model.match as m
import server.model.event as e
from server.model.schedule import insert_sched

engine = server.model.connection.engine

#todo(stacy) Split schedule and match results logic.
# Loading competition schedules is season-independent. Loading match
# results is not (depends on season). Put the logic in two different
# modules with season-dependent logic in server.season package. Also,
# these two processes should not be started by a single HTTP call -
# There should be two different cherry-py exposed methods, one
# for loading schedule and one for loading season results. This will
# facilitate system testing.


#todo(stacy) insert_all_events to server.model.schedule.py
def insert_all_events(season, tournamentLevel, fileName = '-1'):
    if fileName == '-1':
        event_json = api.events(season, tournamentLevel)

    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        event_json = open(fileName).read()

    process_all_events(season, event_json, tournamentLevel)


#todo(stacy) process_all_events to server.model.schedule.py
def process_all_events(season, event_json, tournamentLevel):
    eve = json.loads(event_json)['Events']
    initial_event = e.EventDal.get_current_event()[1]
    print('Initial event is ' + initial_event)
    for event in eve:
        loading_event = event['code']
        print('Setting current event to ' + loading_event)
        e.EventDal.set_current_event(loading_event, season)
        print("insert sched for " + loading_event)
        insert_sched(event['code'], season, tournamentLevel)
    for event in eve:
        loading_event = event['code']
        print('Setting current event to ' + loading_event)
        print("load match results for " + loading_event)
        insert_MatchResults(loading_event, season, tournamentLevel)

    print('Resetting current event to ' + initial_event)
    e.EventDal.set_current_event(initial_event, season)


#todo(stacy) insert_MatchResults to server.model.schedule.py
def insert_MatchResults(event, season, tournamentLevel, fileName = '-1'):
    event = event.lower()
    if fileName == '-1':
        score_json = api.match_scores(event, season, tournamentLevel)

    else:
        fpath = os.path.dirname(os.path.abspath(__file__))
        os.chdir(fpath)
        testJsonPath = '../TestJson'
        os.chdir(testJsonPath)
        score_json = open(fileName).read()
        process_match_results(event, season, tournamentLevel, score_json)

    process_match_results(event, season, tournamentLevel, score_json)


#todo(stacy) process_match_results to module in server.season
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


#todo(stacy) load_robot_movebaseline to module in server.season
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
    m.MatchDal.insert_match_task(team1, "moveBaseline", match, "auto", 0, attempt_count, success_count)


#todo(stacy) load_alliance_rotors to module in server.season
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

    m.MatchDal.insert_alliance_task(alliance, task, phase, match, 0, attempt_count, success_count, 0)


#todo(stacy) load_alliance_flag to module in server.season
def load_alliance_flag(event, match, alnce, firstApiTaskName, taskName, phase):
    Value = alnce[firstApiTaskName]
    alliance = alnce['alliance'].lower()
    success_count = 0
    attempt_count = 1
    if Value:
        success_count = 1
    m.MatchDal.insert_alliance_task(alliance, taskName, phase, match, 0, attempt_count, success_count)


#todo(stacy) load_alliance_measure to module in server.season
def load_alliance_measure(event, match, alnce, firstApiTaskName, taskName, phase):
    Value = alnce[firstApiTaskName]
    alliance = alnce['alliance'].lower()
    success_count = Value
    attempt_count = Value
    m.MatchDal.insert_alliance_task(alliance, taskName, phase, match, 0, attempt_count, success_count)
