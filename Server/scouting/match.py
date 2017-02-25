import event
import dimension
import json
import db
from sqlalchemy import text

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

    def __init__(self):
        pass

    def matchteams(self, station, team):
        pass

    def matchteamtasks(self, match, team, phase):
        current_match = event.EventDal.current_match(match, team)
        event_id = self.events[current_match['event']]
        match_id = self.matches[match]
        team_id = self.teams[team]
        phase_id = self.phases[phase]
        conn.execute(
            "SELECT * FROM measures " +
            "WHERE " +
            " event_id = :event_id" +
            " AND match_id = :match_id" +
            " AND team_id = :team_id " +
            " AND phase_id = :phase_id;",
        event_id=event_id, match_id=match_id,team_id=team_id,phase_id=phase_id)
        #todo add prepared statement parameters
        results = conn.fetchall()
        measures = []
        for measure in results:
            measures.append(dict(measure))
        return json.dumps(measures)

    @staticmethod
    def matchteamtask(match, team, task, phase, value):
        # find the parameter ids for match team task phase-- make a map
        match_id = MatchDal.matches[match]
        team_id = MatchDal.teams[team]
        phase_id = MatchDal.phases[phase]
        task_id = MatchDal.tasks[task]
        # find ids event date alliance station from the schedule table --make a map
        current_match = event.EventDal.current_match(match, team)
        date_id = MatchDal.dates[current_match['date']]
        event_id = MatchDal.events[current_match['event']]
        level_id = MatchDal.events[current_match['level']]
        alliance_id = MatchDal.alliances[current_match['alliance']]
        station_id = MatchDal.stations[current_match['station']]

        # match status is equal to current (call event.current_match)
        # convert the event date alliance station to appropriate ids
        # find the actor and measuretype for the given task and phase

        # look up summary attempt id and the na reason id
        attempt_id = MatchDal.attempts['summary']
        reason_id = MatchDal.reasons['na']

        # based on measure type, set the value (capability, attempt, success, cycle_time)

        # call the upsert
        # insert into mea)sures (event_id, match_id, alliance_id, team_ikd, station_id, actor_id task_id, measture_type_id, phasee_id, attmept_id, reason_id, capability, attempts, sucsuccess, cycle_time)
        # values (:event_id, : ...)
        # on conflict update measures set capability = :capability, attempts = attempats + :attempts, sccess = success + :success, cycle_time)
        # where event_id = :event_id and match_id = :match_id, ... and reason_id = :reason_id

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
            "success, "
            "cycle_time"
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
            ":success, "
            ":cycle_time )" +
            " ON CONFLICT (measures) DO UPDATE "
            "SET capability= :capability, attempts= attempts + :attempts, "
            "success= success +:success, cycle_time=:cycle_time"
            " WHERE "
            "date_id = :date_id "
            "AND event_id = :event_id "
            "AND level_id = :level_id "
            "AND match_id = :match_id "
            "AND alliance_id = :alliance_id "
            "AND team_id= :team_id "
            "AND station_id = :station_id "
            "AND actor_id =:actor_id "
            "AND task_id =:task_id "
            "AND measuretype_id =:measuretype_id "
            "AND phase_id =:phase_id "
            "AND attempt_id= :attempt_id "
            "AND reason_id =:reason_id;")
        conn.execute(sql,
        date_id=date_id,event_id=event_id,level_id=level_id,match_id=match_id,alliance_id=alliance_id,team_id=team_id,station_id=station_id,
        actor_id=actor_id,task_id=task_id,measuretype_id=measuretype_id,phase_id=phase_id,attempt_id=attempt_id,reason_id=reason_id,
        capability=0,attempts=0,success=0,cycle_time=0)
        #todo add prepared statement parameters

