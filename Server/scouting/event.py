import psycopg2
import psycopg2.extras

conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

class EventDal(object):

    def current_match(self, match, team):
        cur.execute("SELECT * FROM schedules WHERE "
                    "match_status = 'current' "
                    " AND team = " + team
                    + "AND match = " + match + ";")
        event = cur.fetchall()
        current_match = []
        for row in event:
            current_match.append(dict(row))
        return current_match