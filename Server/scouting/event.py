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