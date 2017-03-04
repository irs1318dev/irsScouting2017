from collections import OrderedDict

import event
import dimension
import json
import db
from sqlalchemy import text
import game

engine = db.getdbengine()
conn = engine.connect()


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

    def matchteams(self, match):
        pass

    @staticmethod
    def matchteamtasks(match, team, phase):
        match_id = MatchDal.matches[match]
        team_id = MatchDal.teams[team]
        phase_id = MatchDal.phases[phase]

        evt = event.EventDal.getCurrentEvent()
        event_id = MatchDal.events[evt]

        sql = text("SELECT * FROM measures WHERE "
                    "event_id = :event_id "
                    "AND match_id = :match_id "
                    "AND team_id = :team_id;")

        results = conn.execute(sql, event_id=event_id, match_id=match_id,
                               team_id=team_id, phase_id=phase_id).fetchall()
        mt_tasks = []
        for row in results:
            task = MatchDal.task_ids[row['task_id']]
            actor = MatchDal.actor_ids[row['actor_id']]
            measuretype = MatchDal.measturetype_ids[row['measuretype_id']]
            capability = row['capability']
            attempts = row['attempts']
            successes = row['successes']
            cycle_times = row['cycle_times']

            mt_tasks.append(OrderedDict([('match', match), ('team', team), ('task', task), ('phase', phase),
                           ('actor', actor), ('measuretype', measuretype), ('capability', capability),
                           ('attempts', attempts), ('successes', successes), ('cycle_times', cycle_times)]))

        return json.dumps(mt_tasks)


    @staticmethod
    def matchteamtask(team, task, match='na', phase='claim', capability=0, attempt_count=0, success_count=0,
                      cycle_time=0):
        event_name = event.EventDal.getCurrentEvent()
        event_id = MatchDal.events[event_name]

        match_id = MatchDal.matches[match]

        team_id = MatchDal.teams[team]
        phase_id = MatchDal.phases[phase]
        task_id = MatchDal.tasks[task]
        actor_measure = game.GameDal.getActorMeasure(task, phase)
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
            "SET capability=:capability, attempts=measures.attempts + :attempts, "
            "successes=measures.successes + :successes, cycle_times=:cycle_times;")
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
            return capability, 0, 0, 0, attempt_id
        elif measure == 'enum':
            task_option = '{}-{}'.format(task_name, capability)
            option_id = MatchDal.task_option_ids[task_option]
            return option_id, 0, 0, 0, attempt_id
        elif measure == 'attempt':
            return 0
        elif measure == 'cycletime':
            return 0


