import scouting.db as db
from sqlalchemy import text

engine = db.getdbengine()
conn = engine.connect()

# conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class EventDal(object):

    @staticmethod
    def current_match(match, team):
        sql = text("SELECT * FROM schedules WHERE "
                    "match_status = 'current' "
                    " AND team = :team "
                    + " AND match = :match;")
        event = conn.execute(sql,team=team,match=match)
        current_match = []
        for row in event:
            current_match.append(dict(row))
        return current_match