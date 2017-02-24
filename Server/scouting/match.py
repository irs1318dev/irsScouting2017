import psycopg2
import psycopg2.extras
import event
import dimension
import json
conn = psycopg2.connect("dbname=scouting host=localhost user=irs1318 password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class MatchDal(object):

    dates, date_ids = dimension.find_id("dates")
    events, event_ids = dimension.find_id("events")
    levels, level_ids = dimension.find_id("levels")
    matches, match_ids = dimension.find_id("matches")
    alliances, alliance_ids = dimension.find_id("alliances")
    teams, team_ids = dimension.find_id("teams")
    stations, stations_ids = dimension.find_id("stations")
    actors, actor_ids = dimension.find_id("actors")
    tasks, task_ids = dimension.find_id("tasks")
    measuretypes, measturetype_ids = dimension.find_id("measuretypes")
    phases, phase_ids = dimension.find_id("phases")
    attempts, attempt_ids = dimension.find_id("attempts")
    reasons, reasons_ids = dimension.find_id("reasons")

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
        cur.execute(
            "SELECT * FROM measures " +
            "WHERE " +
            " event_id = :event_id" +
            " AND match_id = :match_id" +
            " AND team_id = :team_id " +
            " AND phase_id = :phase_id;")
        #todo add prepared statement parameters
        results = cur.fetchall()
        measures = []
        for measure in results:
            measures.append(dict(measure))
        return json.dump(measures)

    def matchteamtask(self, match, team, task, phase, value):
        # find the parameter ids for match team task phase-- make a map
        match_id = self.matches[match]
        team_id = self.teams[team]
        phase_id = self.phases[phase]
        task_id = self.tasks[task]
        # find ids event date alliance station from the schedule table --make a map
        current_match = event.current_match(match, team)
        date_id = self.dates[current_match['date']]
        event_id = self.events[current_match['event']]
        alliance_id = self.alliances[current_match['alliance']]
        station_id = self.stations[current_match['station']]

        # match status is equal to current (call event.current_match)
        # convert the event date alliance station to appropriate ids
        # find the actor and measuretype for the given task and phase

        # look up summary attempt id and the na reason id
        attempt_id = self.attempts['summary']
        reason_id = self.reasons['na']

        # based on measure type, set the value (capability, attempt, success, cycle_time)

        # call the upsert
        # insert into mea)sures (event_id, match_id, alliance_id, team_ikd, station_id, actor_id task_id, measture_type_id, phasee_id, attmept_id, reason_id, capability, attempts, sucsuccess, cycle_time)
        # values (:event_id, : ...)
        # on conflict update measures set capability = :capability, attempts = attempats + :attempts, sccess = success + :success, cycle_time)
        # where event_id = :event_id and match_id = :match_id, ... and reason_id = :reason_id
        cur.execute(
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
        #todo add prepared statement parameters

