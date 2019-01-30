"""

"""
# helpful SELECT * FROM measures m, alliances a, teams t, tasks s
#   WHERE a.name = 'red' and t.name = 'na' and s.name = 'finalScore'
#   and m.alliance_id = a.id and m.team_id = t.id and m.task_id = s.id;

import json
from collections import OrderedDict

from sqlalchemy import text

import server.model.connection
import server.model.dal as sm_dal
import server.model.event as event
import server.scouting.game as game

engine = server.model.connection.engine


#todo(stacy) Consider doing JSON transformation for tablets in View section.
class MatchDal(object):

    @staticmethod
    def match_teams(match):
        """Retrieves teams assigned to match passed in `match` argument.

        Args:
            match: (str) Match number formatted as "nnn-p|q" (the
            vertical bar means either 'p' or 'q' is acceptable). For
            example, 001-q, 034-q, 103-q, or 003-p. "q" denotes a
            qualificaiton match and "p" denotes a playoff match.

        Returns:
            JSON string in following format:
            {"alliance": "red", "match": "nnn-p|q",
                "team1": nnnn, "team2", nnnn, "team3": nnnn}\n
            {"alliance": "blue", "match": "nnn-p|q",
                "team1": nnnn, "team2", nnnn, "team3": nnnn}
        """
        match_teams = []
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND event_id = :evt_id ")
        conn = engine.connect()
        results = conn.execute(sql,
                               evt_id=event.EventDal.get_current_event()[0],
                               match=match)
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

        # todo(stacy) Is separator ("\n") needed at end?
        out = json.dumps(red, default=lambda o: o.__dict__,
                         separators=(', ', ':'), sort_keys=True) + '\n'
        out += json.dumps(blue, default=lambda o: o.__dict__,
                          separators=(', ', ':'), sort_keys=True) + '\n'
        return out

    @staticmethod
    def pit_teams():
        """Returns JSON list of teams sheduled to compete.

        Returns: (str) JSON string with following format:
        {"match":"na", "teams":["nnnn", "nnnn", ...,  "na"]}
        """
        pit_teams = ''
        sql = text("SELECT DISTINCT team FROM schedules WHERE "
                   "event_id = :evt_id ORDER BY team;")

        conn = engine.connect()
        results = conn.execute(sql,
                               evt_id=event.EventDal.get_current_event()[0])
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
    def match_team_tasks(match, team):
        """Gets JSON string of all measures for specific team and match.

        Returns measures for whichever event is set as the current
        event. To set the current event, call
        `server.model.event.EventDal.set_current_event("event_code").

        Args:
            match: (str) Match number, e.g., "034-q" or "002-p"
            team: (str) FRC team number, e.g., 1318 or 360.

        Returns: Several JSON strings combined into a single string,
        with each string separated by a carriage return ('\n').
        Each individual JSON string is in the following format:

            {"match": "nnn-p|q", "team": "nnnn", "task": "{task_name}",
            "phase": "{phase}", "actor": "{actor}",
            "measuretype": "{measuretype}", "capability": 0|1,
            "attempts": {int}, "successes": {int},
            "cycle_times": {int}}
        """
        # todo(stacy) add optional event argument.
        match_id = sm_dal.match_ids[match]
        team_id = sm_dal.team_ids[team]

        event_id = event.EventDal.get_current_event()[0]


        sql = text("""
                    SELECT * FROM measures WHERE
                    event_id = :event_id
                    AND match_id = :match_id
                    AND team_id = :team_id;
                    """)

        conn = engine.connect()
        results = conn.execute(sql, event_id=event_id, match_id=match_id,
                               team_id=team_id).fetchall()
        conn.close()

        out = ''
        for row in results:
            task = sm_dal.task_names[row['task_id']]
            actor = sm_dal.actor_names[row['actor_id']]
            phase = sm_dal.phase_names[row['phase_id']]
            measuretype = sm_dal.measuretype_names[row['measuretype_id']]
            capability = row['capability']
            attempts = row['attempts']
            successes = row['successes']
            cycle_times = row['cycle_times']

            if capability > 0:
                capability = sm_dal.task_option_options[capability]

            out += (json.dumps(OrderedDict([('match', match), ('team', team),
                                            ('task', task), ('phase', phase),
                                            ('actor', actor),
                                            ('measuretype', measuretype),
                                            ('capability', capability),
                                            ('attempts', attempts),
                                            ('successes', successes),
                                            ('cycle_times', cycle_times)])) +
                    '\n')

        return out

    @staticmethod
    def insert_match_task(team, task, match='na', phase='claim', capability=0,
                          attempt_count=0, success_count=0, cycle_time=0):
        """Insert data on a task into the database.

        Args:
            team: (str) FRC team number
            task: (str) Name of task
            match: (str) Match number in nnn-p|q format
            phase: (str) Name of phase
            capability: (int) 1 if has capability, 0 if not
            attempt_count: (int) Number of attempts, successful or not
            success_count: (int) Number of successes
            cycle_time: (int) Number of seconds
        """
        # Get ID value for current event
        curr_event = event.EventDal.get_current_event()
        # Get ID values for arguments
        team_id = sm_dal.team_ids[team]
        task_id = sm_dal.task_ids[task]
        match_id = sm_dal.match_ids[match]
        phase_id = sm_dal.phase_ids[phase]
        # Get season-specific data and IDs
        actor_measure = game.GameDal.get_actor_measure(task, phase)
        actor_id = sm_dal.actor_ids[actor_measure["actor"]]
        measure = actor_measure[phase]
        measuretype_id = sm_dal.measuretype_ids[measure]
        # Get additional match details
        match_details = event.EventDal.match_details(curr_event[1],
                                                     curr_event[2], match, team)
        date_id = sm_dal.date_ids[match_details['date']]
        level_id = sm_dal.level_ids[match_details['level']]
        alliance_id = sm_dal.alliance_ids[match_details['alliance']]
        station_id = sm_dal.station_ids[match_details['station']]
        reason_id = sm_dal.reason_ids['na']

        (capability, attempt_count, success_count, cycle_time,
         attempt_id) = MatchDal._transform_measure(measure, capability,
                                                   attempt_count,
                                                   success_count,
                                                   cycle_time, task)

        sql = text(
            "INSERT INTO measures "
            "(date_id, event_id, level_id, match_id, alliance_id, "
            "team_id, station_id, actor_id, task_id, measuretype_id, "
            "phase_id, attempt_id, reason_id, capability, attempts, "
            "successes, cycle_times) "
            
            "VALUES("
            ":date_id, :event_id, :level_id, :match_id, :alliance_id, "
            ":team_id, :station_id, :actor_id, :task_id, :measuretype_id, "
            ":phase_id, :attempt_id, :reason_id, :capability, :attempts, "
            ":successes, :cycle_times) "
            
            "ON CONFLICT ON CONSTRAINT measures_pkey DO UPDATE "
            "SET capability=:capability, attempts=:attempts, "
            "successes=:successes, cycle_times=:cycle_times;")
        conn = engine.connect()
        conn.execute(sql, date_id=date_id, event_id=curr_event[0],
                     level_id=level_id, match_id=match_id,
                     alliance_id=alliance_id, team_id=team_id,
                     station_id=station_id, actor_id=actor_id,
                     task_id=task_id, measuretype_id=measuretype_id,
                     phase_id=phase_id, attempt_id=attempt_id,
                     reason_id=reason_id, capability=capability,
                     attempts=attempt_count, successes=success_count,
                     cycle_times=cycle_time)
        conn.close()

    @staticmethod
    def insert_alliance_task(alliance, task, phase, match, capability=0,
                             attempt_count=0, success_count=0,
                             cycle_time=0):
        """Inserts task for an alliance and match, not linked to team.

        Only works if schedule loaded for event.

        Args:
            alliance: (str) "red" or "blue"
            task: (str) Name of task
            phase: (str) Name of phase
            match: (str) Match number in nnn-p|q format
            capability: (int) 1 if has capability, 0 if not
            attempt_count: (int) Number of attempts, successful or not
            success_count: (int) Number of successes
            cycle_time: (int) Number of seconds
        """
        curr_event = event.EventDal.get_current_event()
        event_name = curr_event[1]
        event_id = curr_event[0]
        event_season = curr_event[2]

        match_id = sm_dal.match_ids[match]

        team_id = sm_dal.team_ids['na']
        phase_id = sm_dal.phase_ids[phase]
        task_id = sm_dal.task_ids[task]
        actor_measure = game.GameDal.get_actor_measure(task, phase)
        actor_id = sm_dal.actor_ids[actor_measure["actor"]]
        measure = actor_measure[phase]
        measuretype_id = sm_dal.measuretype_ids[measure]
        alliance_id = sm_dal.alliance_ids[alliance]
        station_id = sm_dal.station_ids['na']

        match_details = event.EventDal.match_alliance_details(event_name,
                                                              event_season,
                                                              match)
        date_id = sm_dal.date_ids[match_details['date']]
        level_id = sm_dal.level_ids[match_details['level']]

        reason_id = sm_dal.reason_ids['na']

        capability, attempt_count, success_count, cycle_time, attempt_id = \
            MatchDal._transform_measure(measure, capability, attempt_count,
                                        success_count, cycle_time, task)

        sql = text(
            "INSERT INTO measures "
            "(date_id, event_id , level_id, match_id ,alliance_id, team_id, "
            "station_id, actor_id, task_id , measuretype_id ,phase_id, "
            "attempt_id , reason_id, capability, attempts, successes, "
            "cycle_times) "
            "VALUES"
            "(:date_id, :event_id, :level_id, :match_id, :alliance_id, "
            ":team_id, :station_id, :actor_id, :task_id, :measuretype_id, "
            ":phase_id, :attempt_id, :reason_id, :capability, :attempts, "
            ":successes, :cycle_times ) " +
            "ON CONFLICT ON CONSTRAINT measures_pkey DO UPDATE "
            "SET capability=:capability, attempts=:attempts, "
            "successes=:successes, cycle_times=:cycle_times;")
        conn = engine.connect()
        conn.execute(sql,
                     date_id=date_id, event_id=event_id, level_id=level_id,
                     match_id=match_id, alliance_id=alliance_id,
                     team_id=team_id, station_id=station_id,
                     actor_id=actor_id, task_id=task_id,
                     measuretype_id=measuretype_id, phase_id=phase_id,
                     attempt_id=attempt_id, reason_id=reason_id,
                     capability=capability, attempts=attempt_count,
                     successes=success_count, cycle_times=cycle_time)
        conn.close()

# todo(stacy) Talk to Stuart about this function
    @staticmethod
    def _transform_measure(data_type, capability, attempt_count, success_count,
                           cycle_time, task_name):
        """

        Args:
            data_type: (str) Either "na", "count", "percentage", "boolean",
                "enum", "attempt" or "cycletime".
            capability:
            attempt_count:
            success_count:
            cycle_time:
            task_name:

        Returns:
            A Python tuple: (capability, attempt_count, success_count,
            cycle_time, attempt_id)

        Enums:
            if statement added because sometimes the capability can be passed in as a blank string when resseting/removing it
        """
        attempt_id = sm_dal.attempt_ids['summary']
        if data_type == 'na':
            return 0, 0, 0, 0, attempt_id
        elif data_type == 'count':
            return 0, attempt_count, success_count, 0, attempt_id
        elif data_type == 'percentage':
            if capability == '':
                return 0, 0, 0, 0, attempt_id
            if (int)(capability) < 0:
                capability = '0'
                return 0, 0, 0, capability, attempt_id
            if (int)(capability) > 100:
                capability = '100'
                return 0, 0, 0, capability, attempt_id
            return 0, 0, 0, capability, attempt_id
        elif data_type == 'boolean':
            return 0, attempt_count, success_count, 0, attempt_id
        elif data_type == 'enum':
            if capability == '':
                option_id = 0
            else:
                task_option = '{}-{}'.format(task_name, capability)
                option_id = sm_dal.task_option_ids[task_option]
            return option_id, 0, 0, 0, attempt_id
        elif data_type == 'attempt':
            return 0
        elif data_type == 'cycletime':
            return 0
        elif data_type == 'rating':
            return 0, attempt_count, success_count, 0, attempt_id


# todo(Stacy) This could easily be replaced with Python dictionary
class TabletMatch(object):
    """Specifies the 3 teams assigned to alliance for a specific match.

    This class is used in match)_teams function to generate JSON text
    to send to tablets.
    """
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

# todo(Stacy) Not used anywhere - consider eliminating
class PitMatch(object):
    def __init__(self, teams):
        self.match = 'na'
        self.teams = teams


