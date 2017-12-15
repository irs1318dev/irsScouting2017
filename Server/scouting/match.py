from collections import OrderedDict

import scouting.event as event
import scouting.dimension as dimension
import json
import scouting.db as db
from sqlalchemy import text
import scouting.game as game

engine = db.getdbengine()


class MatchDal(object):
    dates, date_ids = dimension.DimensionDal.build_dimension_dicts("dates")
    events, event_ids = dimension.DimensionDal.build_dimension_dicts("events")
    levels, level_ids = dimension.DimensionDal.build_dimension_dicts("levels")
    matches, match_ids = dimension.DimensionDal.build_dimension_dicts("matches")
    alliances, alliance_ids = dimension.DimensionDal.build_dimension_dicts("alliances")
    teams, team_ids = dimension.DimensionDal.build_dimension_dicts("teams")
    stations, stations_ids = dimension.DimensionDal.build_dimension_dicts("stations")
    actors, actor_ids = dimension.DimensionDal.build_dimension_dicts("actors")
    tasks, task_ids = dimension.DimensionDal.build_dimension_dicts("tasks")
    measuretypes, measturetype_ids = dimension.DimensionDal.build_dimension_dicts("measuretypes")
    phases, phase_ids = dimension.DimensionDal.build_dimension_dicts("phases")
    attempts, attempt_ids = dimension.DimensionDal.build_dimension_dicts("attempts")
    reasons, reasons_ids = dimension.DimensionDal.build_dimension_dicts("reasons")
    task_options, task_option_ids = dimension.DimensionDal.build_task_option_dicts()

    def __init__(self):
        pass

    @staticmethod
    def matchteams(match):
        match_teams = []
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND event = :event ")
        conn = engine.connect()
        results = conn.execute(sql, event=event.EventDal.get_current_event(), match=match)
        conn.close()

        for row in results:
            match_teams.append(dict(row))

        red = TabletMatch("red")
        blue = TabletMatch("blue")

        for line in match_teams:
            if line['alliance'] == 'red':
                red.teamadd(line['team'], line['match'])
            if line['alliance'] == 'blue':
                blue.teamadd(line['team'], line['match'])

        out = json.dumps(red, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True) + '\n'
        out += json.dumps(blue, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True) + '\n'
        return out

    @staticmethod
    def pitteams():
        pit_teams = ''
        sql = text("SELECT DISTINCT team FROM schedules WHERE "
                   "event = :event ORDER BY team;")

        conn = engine.connect()
        results = conn.execute(sql, event=event.EventDal.get_current_event())
        conn.close()

        first = True
        for row in results:
            if first:
                pit_teams += '"' + str(row).split('\'')[1] + '"'
                first = False
            else:
                pit_teams += ',"' + str(row).split('\'')[1] + '"'

        return '''{"match":"na", "teams":[''' + pit_teams + ']}'

    @staticmethod
    def matchteamtasks(match, team):
        match_id = MatchDal.matches[match]
        team_id = MatchDal.teams[team]

        evt = event.EventDal.get_current_event()
        event_id = MatchDal.events[evt]

        sql = text("SELECT * FROM measures WHERE "
                    "event_id = :event_id "
                    "AND match_id = :match_id "
                    "AND team_id = :team_id;")

        conn = engine.connect()
        results = conn.execute(sql, event_id=event_id, match_id=match_id,
                               team_id=team_id).fetchall()
        conn.close()

        out = ''
        for row in results:
            task = MatchDal.task_ids[row['task_id']]
            actor = MatchDal.actor_ids[row['actor_id']]
            phase = MatchDal.phase_ids[row['phase_id']]
            measuretype = MatchDal.measturetype_ids[row['measuretype_id']]
            capability = row['capability']
            attempts = row['attempts']
            successes = row['successes']
            cycle_times = row['cycle_times']

            if capability > 0 and not capability == 100:
                capability = MatchDal.task_option_ids[capability].split('-')[1]

            out += json.dumps(OrderedDict([('match', match), ('team', team), ('task', task), ('phase', phase),
                           ('actor', actor), ('measuretype', measuretype), ('capability', capability),
                           ('attempts', attempts), ('successes', successes), ('cycle_times', cycle_times)])) + '\n'

        return out

    @staticmethod
    def matchteamtask(team, task, match='na', phase='claim', capability=0, attempt_count=0, success_count=0,
                      cycle_time=0):
        event_name = event.EventDal.get_current_event()
        event_id = MatchDal.events[event_name]

        match_id = MatchDal.matches[match]

        team_id = MatchDal.teams[team]
        phase_id = MatchDal.phases[phase]
        task_id = MatchDal.tasks[task]
        actor_measure = game.GameDal.get_actor_measure(task, phase)
        actor_id = MatchDal.actors[actor_measure["actor"]]
        measure = actor_measure[phase]
        measuretype_id = MatchDal.measuretypes[measure]

        match_details = event.EventDal.match_details(event_name, match, team)
        date_id = MatchDal.dates[match_details['date']]
        level_id = MatchDal.levels[match_details['level']]
        alliance_id = MatchDal.alliances[match_details['alliance']]
        station_id = MatchDal.stations[match_details['station']]

        reason_id = MatchDal.reasons['na']

        capability, attempt_count, success_count, cycle_time, attempt_id = \
            MatchDal.transform_measure(measure, capability, attempt_count,
                                       success_count, cycle_time, task)

        sql = text(
            "INSERT INTO measures "
            "( "
            "date_id, "
            "event_id , "
            "level_id, "
            "match_id ,"
            "alliance_id, "
            "team_id, "
            "station_id, "
            "actor_id, "
            "task_id , "
            "measuretype_id ,"
            "phase_id, "
            "attempt_id , "
            "reason_id, "
            "capability, "
            "attempts, "
            "successes, "
            "cycle_times"
            ") "
            " VALUES("
            ":date_id, "
            ":event_id, "
            ":level_id, "
            ":match_id, "
            ":alliance_id, "
            ":team_id, "
            ":station_id, "
            ":actor_id, "
            ":task_id, "
            ":measuretype_id, "
            ":phase_id, "
            ":attempt_id, "
            ":reason_id, "
            ":capability, "
            ":attempts, "
            ":successes, "
            ":cycle_times )" +
            " ON CONFLICT ON CONSTRAINT measures_pkey DO UPDATE "
            "SET capability=:capability, attempts=:attempts, "
            "successes=:successes, cycle_times=:cycle_times;")
        conn = engine.connect()
        conn.execute(sql,
                     date_id=date_id,
                     event_id=event_id,
                     level_id=level_id,
                     match_id=match_id,
                     alliance_id=alliance_id,
                     team_id=team_id,
                     station_id=station_id,
                     actor_id=actor_id,
                     task_id=task_id,
                     measuretype_id=measuretype_id,
                     phase_id=phase_id,
                     attempt_id=attempt_id,
                     reason_id=reason_id,
                     capability=capability,
                     attempts=attempt_count,
                     successes=success_count,
                     cycle_times=cycle_time)
        conn.close()

    @staticmethod
    def matchalliancetask(alliance, task, phase, match='na', capability=0, attempt_count=0, success_count=0,
                      cycle_time=0):
        event_name = event.EventDal.get_current_event()
        event_id = MatchDal.events[event_name]

        match_id = MatchDal.matches[match]

        team_id = MatchDal.teams['na']
        phase_id = MatchDal.phases[phase]
        task_id = MatchDal.tasks[task]
        actor_measure = game.GameDal.get_actor_measure(task, phase)
        actor_id = MatchDal.actors[actor_measure["actor"]]
        measure = actor_measure[phase]
        measuretype_id = MatchDal.measuretypes[measure]
        alliance_id = MatchDal.alliances[alliance]
        station_id = MatchDal.stations['na']

        match_details = event.EventDal.match_alliance_details(event_name, match)
        date_id = MatchDal.dates[match_details['date']]
        level_id = MatchDal.levels[match_details['level']]

        reason_id = MatchDal.reasons['na']

        capability, attempt_count, success_count, cycle_time, attempt_id = \
            MatchDal.transform_measure(measure, capability, attempt_count,
                                       success_count, cycle_time, task)

        sql = text(
            "INSERT INTO measures "
            "( "
            "date_id, "
            "event_id , "
            "level_id, "
            "match_id ,"
            "alliance_id, "
            "team_id, "
            "station_id, "
            "actor_id, "
            "task_id , "
            "measuretype_id ,"
            "phase_id, "
            "attempt_id , "
            "reason_id, "
            "capability, "
            "attempts, "
            "successes, "
            "cycle_times"
            ") "
            " VALUES("
            ":date_id, "
            ":event_id, "
            ":level_id, "
            ":match_id, "
            ":alliance_id, "
            ":team_id, "
            ":station_id, "
            ":actor_id, "
            ":task_id, "
            ":measuretype_id, "
            ":phase_id, "
            ":attempt_id, "
            ":reason_id, "
            ":capability, "
            ":attempts, "
            ":successes, "
            ":cycle_times )" +
            " ON CONFLICT ON CONSTRAINT measures_pkey DO UPDATE "
            "SET capability=:capability, attempts=:attempts, "
            "successes=:successes, cycle_times=:cycle_times;")
        conn = engine.connect()
        conn.execute(sql,
                     date_id=date_id,
                     event_id=event_id,
                     level_id=level_id,
                     match_id=match_id,
                     alliance_id=alliance_id,
                     team_id=team_id,
                     station_id=station_id,
                     actor_id=actor_id,
                     task_id=task_id,
                     measuretype_id=measuretype_id,
                     phase_id=phase_id,
                     attempt_id=attempt_id,
                     reason_id=reason_id,
                     capability=capability,
                     attempts=attempt_count,
                     successes=success_count,
                     cycle_times=cycle_time)
        conn.close()

    @staticmethod
    def transform_measure(measure, capability, attempt_count, success_count, cycle_time, task_name):
        attempt_id = MatchDal.attempts['summary']
        if measure == 'na':
            return 0, 0, 0, 0, attempt_id
        elif measure == 'count':
            return 0, attempt_count, success_count, 0, attempt_id
        elif measure == 'percentage':
            return capability, 0, 0, 0, attempt_id
        elif measure == 'boolean':
            return 0, attempt_count, success_count, 0, attempt_id
        elif measure == 'enum':
            task_option = '{}-{}'.format(task_name, capability)
            option_id = MatchDal.task_options[task_option]
            return option_id, 0, 0, 0, attempt_id
        elif measure == 'attempt':
            return 0
        elif measure == 'cycletime':
            return 0


class TabletMatch(object):
    def __init__(self, alliance):
        self.alliance = alliance
        self.match = ''
        self.team1 = ''
        self.team2 = ''
        self.team3 = ''

    def teamadd(self, name, match):
        if self.match is '':
            self.match = match
        if self.team1 is '':
            self.team1 = name
        else:
            if self.team2 is '':
                self.team2 = name
            else:
                if self.team3 is '':
                    self.team3 = name


class PitMatch(object):
    def __init__(self, teams):
        self.match = 'na'
        self.teams = teams



# helpful SELECT * FROM measures m, alliances a, teams t, tasks s WHERE a.name = 'red' and t.name = 'na' and s.name = 'finalScore' and m.alliance_id = a.id and m.team_id = t.id and m.task_id = s.id;