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
                   " AND event = :event " )
        results = conn.execute(sql,event=event,
                               match=match, team=team)
        for row in results:
            match_details = dict(row)
        return match_details

    @staticmethod
    def match_teams(event, match):
        match_details = {}
        sql = text("SELECT * FROM schedules WHERE "
                   "match = :match "
                   " AND event = :event ")
        results = conn.execute(sql, event=event, match=match)
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
            conn.execute(sql_upd, event = event, id = results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (event) VALUES (:event);")
            conn.execute(sql_ins, event = event)

    @staticmethod
    def get_current_event():
        sql = text("SELECT event FROM status;")
        return conn.execute(sql).scalar()

    @staticmethod
    def set_current_match(match):
        sql_sel = text("SELECT * FROM status;")
        results = conn.execute(sql_sel).fetchall()
        if len(results) == 1:
            sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
            conn.execute(sql_upd, match = match, id = results[0]['id'])
        elif len(results) == 0:
            sql_ins = text("INSERT INTO status (match) VALUES (:match);")
            conn.execute(sql_ins, match = match)

    @staticmethod
    def get_current_match():
        sql = text("SELECT match FROM status;")
        return conn.execute(sql).scalar()
