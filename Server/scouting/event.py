import scouting.db as db
from sqlalchemy import text

engine = db.getdbengine()
conn = engine.connect()

# conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class EventDal(object):

    @staticmethod
    def match_details(event, match, team):
        match_details = {}
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND team = :team "
                   " AND event = :event ")
        results = conn.execute(sql, event=event, match=match, team=team)
        for row in results:
            match_details = dict(row)
        return match_details

    @staticmethod
    def set_current_event(event):
        event = event.lower()

        sql_sel = text("SELECT * FROM status;")
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET event = :event WHERE id = :id;")
            conn.execute(sql_upd, event=event, id=results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (event) VALUES (:event);")
            conn.execute(sql_ins, event=event)

    @staticmethod
    def get_current_event():
        event = conn.execute("SELECT event FROM status;").scalar()
        if event is None:
            event = conn.execute("SELECT name FROM events LIMIT 1")
            EventDal.set_current_event(event)
        return event

    @staticmethod
    def set_current_match(match):
        sql_sel = text("SELECT * FROM status;")
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
            conn.execute(sql_upd, match=match, id=results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (match) VALUES (:match);")
            conn.execute(sql_ins, match=match)

    @staticmethod
    def set_next_match(match):
        if (match == 'na'):
            return

        # match is in format 001-q
        result = match.split('-')
        nextMatchNumber = int(result[0]) + 1
        nextMatch = "{0:0>3}-q".format(nextMatchNumber)

        sql_sel = text("SELECT * FROM status;")
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
            conn.execute(sql_upd, match=nextMatch, id=results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (match) VALUES (:match);")
            conn.execute(sql_ins, match=nextMatch)


    @staticmethod
    def get_current_match():
        match = conn.execute("SELECT match FROM status;").scalar()
        if match is None:
            match = conn.execute("SELECT name FROM matches LIMIT 1").scalar()
            EventDal.set_current_match(match)
        return match
