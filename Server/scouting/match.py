import psycopg2
import psycopg2.extras
import event
import dimension
conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class MatchDal(object):
    match, match_ids = dimension.find_id("matches")
    team, team_ids = dimension.find_
    def __init__(self):

    def matchteams(self, station, team):

    def matchteamtasks(self, match, team, phase):
        match_id = self.matches[match]
        team_id = self.teams[team]
        phase_id = self.phases[phase]
        cur.execute(
            "SELECT * FROM measures " + "WHERE match_id = " + match_id + " AND team_id = " + team_id + " AND phase_id = " + phase_id + ";")
        ans = cur.fetchall()
        ans1 = []
        for row in ans:
            ans1.append(dict(row))
        return ans1

    def matchteamtask(self, match, team, task, phase, value):
        # find the parameter ids for match team task phase-- make a map
        match_id = self.matches[match]
        team_id = self.teams[team]
        phase_id = self.phases[phase]
        task_id = self.tasks[task]
        # find ids event date alliance station from the schedule table --make a map
        current_match = event.current_match(match, team)
        event_id = self.events[current_match['event']]
        alliance_id = self.alliance[current_match['alliance']]
        station_id = self.station[current_match['station']]
        date_id = self.date[current_match['date']]

        # match status is equal to current (call event.current_match)
        # convert the event date alliance station to appropriate ids
        # find the actor and measuretype for the given task and phase

        # look up summary attempt id and the na reason id
        cur
        attempt_id =

        # based on measure type, set the value (capability, attempt, success, cycle_time)

        # call the upsert
        # insert into mea)sures (event_id, match_id, alliance_id, team_ikd, station_id, actor_id task_id, measture_type_id, phasee_id, attmept_id, reason_id, capability, attempts, sucsuccess, cycle_time)
        # values (:event_id, : ...)
        # on conflict update measures set capability = :capability, attempts = attempats + :attempts, sccess = success + :success, cycle_time)
        # where event_id = :event_id and match_id = :match_id, ... and reason_id = :reason_id
        cur.execute(
            "INSERT INTO measures ( event_id ,  match_id ,alliance_id, team_id, station_id, actor_id, task_id , measuretype_id , phase_id, attempt_id , reason_id, capability, attempts, success, cycle_time) "
            " VALUES(:event_id, :match_id, :alliance_id, :team_id, :station_id, :actor_id, :task_id, :measuretype_id, :phase_id, :attempt_id, :reason_id, :capability, :attempts, :success, :cycle_time )" +
            " ON CONFLICT (measures) DO UPDATE SET capability= :capability, attempts= attempts + :attempts, success= success +:success, cycle_time=:cycle_time"
            " WHERE event_id = :event_id AND match_id = :match_id AND alliance_id = :alliance_id AND team_id= :team_id AND station_id = :station_id AND actor_id =:actor_id AND task_id =:task_id AND measuretype_id =:measuretype_id AND phase_id =:phase_id AND attempt_id= :attempt_id AND reason_id =:reason_id AND capability= :capability AND attempts= :attempts AND success= :success AND cycle_time =:cycle_time ;")
