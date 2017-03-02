import scouting.db as db
from sqlalchemy import text

engine = db.getdbengine()
conn = engine.connect()

curr_event = "waamv"

# conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class EventDal(object):

    @staticmethod
    def current_match(match, team):
        sql = text("SELECT * FROM schedules WHERE "
                    "match_status = 'current' "
                    " AND team = :team "
                    " AND event = :event "
                    + " AND match = :match;")
        results = conn.execute(sql,team=team,match=match,event=curr_event)
        current_match = []
        for row in results:
            current_match.append(dict(row))
        if len(current_match) == 0:
            sql = text("SELECT * FROM schedules WHERE "
                       "match = '001-q' "
                       " AND alliance = 'red' "
                       " AND event = :event "
                       + "AND station = '1';")
            results = conn.execute(sql,event=curr_event)
            for row in results:
                current_match.append(dict(row))
        return current_match


def setCurrentEvent(event):
    event = event.lower()

    sql_sel = text("SELECT * FROM status;")
    results = conn.execute(sql_sel).fetchall()
    if len(results) == 1:
        sql_upd = text("UPDATE status SET event = :event WHERE id = :id;")
        conn.execute(sql_upd, event = event, id = results[0]['id'])
    elif len(results) == 0:
        sql_ins = text("INSERT INTO status (event) VALUES (:event);")
        conn.execute(sql_ins, event = event)

def getCurrentEvent():
    sql = text("SELECT event FROM status;")
    return conn.execute(sql).scalar()

def setCurrentMatch(match):
    sql_sel = text("SELECT * FROM status;")
    results = conn.execute(sql_sel).fetchall()
    if len(results) == 1:
        sql_upd = text("UPDATE status SET match = :match WHERE id = :id;")
        conn.execute(sql_upd, match = match, id = results[0]['id'])
    elif len(results) == 0:
        sql_ins = text("INSERT INTO status (match) VALUES (:match);")
        conn.execute(sql_ins, match = match)

def getCurrentMatch():
    sql = text("SELECT match FROM status;")
    return conn.execute(sql).scalar()
