import json

from sqlalchemy import text

import server.model.dal as sm_dal
from server.model.connection import engine, pool

class EventError(Exception):
    pass

class EventDal(object):

    # # todo(stacy) No usages found
    # @staticmethod
    # def list_events():
    #     events = []
    #     sql = text("SELECT distinct event_id FROM schedules ORDER BY event_id ")
    #     conn = engine.connect()
    #     results = conn.execute(sql)
    #     conn.close()
    #     for row in results:
    #         events.append(dict(row))
    #     print(events)
    #    return events

    # todo(stacy) Shift conversion of Python dictionaries to JSON from DAL to controller (cherry.py methods)
    @staticmethod
    def list_matches(event, season):
        event_id = EventDal.get_event_id(event, season)
        matches = []
        sql = text("SELECT distinct(schedules.match), events.name AS event "
                   "FROM schedules INNER JOIN events "
                   "ON schedules.event_id = events.id "
                   "WHERE schedules.event_id = :evt_id ORDER BY match ")
        conn = engine.connect()
        results = conn.execute(sql, evt_id=event_id)
        conn.close()
        for row in results:
            matches.append(dict(row))
        return json.dumps(matches)

    @staticmethod
    def get_event_id(event, season):
        conn = engine.connect()
        sql = text("SELECT id FROM events "
                   "WHERE name = :evt AND season = :season;")
        event_id = conn.execute(sql, evt=event, season=season).scalar()
        conn.close()
        return event_id

    @staticmethod
    def match_details(event, season, match, team):
        event_id = EventDal.get_event_id(event, season)
        match_details = {}
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND team = :team "
                   " AND event_id = :evt_id ")
        conn = engine.connect()
        results = conn.execute(sql, evt_id=event_id, match=match, team=team)
        conn.close()
        for row in results:
            match_details = dict(row)
        if match_details == {}:
            match_details = {'alliance': 'na', 'level': 'na', 'event': event,
                             'station': 'na', 'team': team, 'date': 'na',
                             'match': match}
        return match_details

    @staticmethod
    def match_details_station(event, match, alliance, station):
        match_details = {}
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND event = :event "
                   " AND alliance = :alliance "
                   " AND station = :station ")
        conn = engine.connect()
        results = conn.execute(sql, event=event, match=match, station=station, alliance=alliance)
        conn.close()
        for row in results:
            match_details = dict(row)
        return match_details

    @staticmethod
    def set_current_event(event, season):
        event = event.lower()
        season = str(season)
        conn = engine.connect()

        # Ensure event exists in events table
        sql_sel = text("SELECT id FROM events "
                       "WHERE name = :evt AND season = :season;")
        events = conn.execute(sql_sel, evt=event, season=season)
        if events.rowcount == 1:
            event_id=events.fetchone()["id"]
        if events.rowcount == 0:
            sql_ins = text("INSERT INTO events (name, season) "
                           "VALUES (:evt, :season);")
            conn.execute(sql_ins, evt=event, season=season)
            sql_sel = text("SELECT id FROM events "
                           "WHERE name = :evt AND season = :season;")
            event_id = conn.execute(sql_sel, evt=event,
                                    season=season).scalar()
            sm_dal.rebuild_dicts() # todo(stacy) might not need this.
        # Update status table with this event
        sql_sel = text("SELECT * FROM status;")
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET event_id = :evt_id "
                           "WHERE id = :id;")
            conn.execute(sql_upd, evt_id=event_id, id=results[0]['id'])
        elif len(results) == 0:
            default_match = "001-q"
            sql_ins = text("INSERT INTO status (event_id, match) "
                           "VALUES (:evt_id, :match);")
            conn.execute(sql_ins, evt_id=event_id, match=default_match)
        conn.close()

        return event_id

    @staticmethod
    def get_current_status():
        sql = text("SELECT * FROM status;")
        conn = engine.connect()
        results = conn.execute(sql)
        conn.close()
        status = dict(results.first())
        return json.dumps(status)

    @staticmethod
    def get_current_event():
        conn = engine.connect()
        event = ("SELECT status.event_id AS event_id, "
                 "events.name AS event_name, events.season AS event_season "
                 "FROM status INNER JOIN events ON status.event_id = events.id")
        results = conn.execute(event)
        if results is None:
            raise EventError(" Event_id not specified in status table."
                             " Fix: Call set_current_event() in event.py")
        evt = results.fetchone()
        conn.close()
        return evt["event_id"], evt["event_name"], evt['event_season']


    @staticmethod
    def set_current_match(match):
        sql_sel = text("SELECT * FROM status;")
        conn = engine.connect()
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
            conn.execute(sql_upd, match=match, id=results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (match) VALUES (:match);")
            conn.execute(sql_ins, match=match)
        conn.close()
        return 'current match '  + match

    @staticmethod
    def set_next_match(match):
        if match == 'na':
            return

        # match is in format 001-q
        result = match.split('-')
        nextMatchNumber = int(result[0]) + 1
        nextMatch = "{0:0>3}-q".format(nextMatchNumber)

        sql_sel = text("SELECT * FROM status;")
        conn = engine.connect()
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
            conn.execute(sql_upd, match=nextMatch, id=results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (match) VALUES (:match);")
            conn.execute(sql_ins, match=nextMatch)
        conn.close()

    @staticmethod
    def get_current_match():
        conn = engine.connect()
        match = conn.execute("SELECT match FROM status;").scalar()
        conn.close()
        if match is None:
            match = "001-q"
            EventDal.set_current_match(match)
        return match


    @staticmethod
    def match_alliance_details(event, season, match):
        event_id = EventDal.get_event_id(event, season)
        match_details = {}
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND event_id = :evt_id ")

        conn = engine.connect()
        results = conn.execute(sql, evt_id=event_id, match=match)
        conn.close()
        for row in results:
            match_details = dict(row)
        return match_details


    @staticmethod
    def get_previous_match():
        match_cur = int(EventDal.get_current_match()[0:3])
        if match_cur == 1:
            return '001-q'
        else:
            return '{:03}-q'.format(match_cur-1)

    @staticmethod
    def last_match_teams():
        event_id = EventDal.get_current_event()[0]
        match_prev = EventDal.get_previous_match()

        sql = '''SELECT team FROM schedules WHERE
                   match = %s
                   AND event_id = %s;'''

        conn = pool.getconn()
        curr = conn.cursor()
        curr.execute(sql, (match_prev, event_id))
        results = curr.fetchall()
        curr.close()
        pool.putconn(conn)
        return [x[0] for x in results]


    @staticmethod
    def team_long_name(team):

        sql = text('''SELECT * FROM teams WHERE name =  :team;''')

        conn = engine.connect()
        results = conn.execute(sql, team=team).fetchone()
        conn.close()
        if len(results) > 0 and results['long_name'] is not None:
            return results['long_name']
        return 'na'

    @staticmethod
    def delete_event(event, season):
        event_id = EventDal.get_event_id(event, season)
        if EventDal.get_current_event()[0] == event_id:
            print("Warning: You cannot delete the current event.")
            return
        sql = text("DELETE FROM measures WHERE event_id = :evt_id")
        conn = engine.connect()
        conn.execute(sql, evt_id=event_id)
        sql = text("DELETE FROM schedules WHERE event_id = :evt_id")
        conn.execute(sql, evt_id=event_id)
        sql = text("DELETE FROM events WHERE id = :evt_id")
        conn.execute(sql, evt_id=event_id)
        conn.close()

    @staticmethod
    def team_match(team):
        sql = '''
              SELECT schedules.match FROM schedules
              INNER JOIN status ON schedules.event_id = status.event_id WHERE team = %s
              ORDER BY schedules.match;'''
        conn = pool.getconn()
        curr = conn.cursor()
        curr.execute(sql, [team])
        matches = [x[0] for x in curr.fetchall()]
        pool.putconn(conn)
        return matches

