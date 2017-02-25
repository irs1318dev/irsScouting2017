import psycopg2.extras

conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


class GameDal(object):

    @staticmethod
    def game(actor, measuretype):
        cur.execute("SELECT * FROM games WHERE "
                    "game = 'current' "
                    " AND actor = " + actor
                    + "AND measuretype = " + measuretype + ";")
        game = cur.fetchall()
         = []
        for row in game:
            .append(dict(row))
        return


class EventDal(object):

    @staticmethod
    def current_match(match, team):
        cur.execute("SELECT * FROM schedules WHERE "
                    "match_status = 'current' "
                    " AND team = " + team
                    + "AND match = " + match + ";")
        event = cur.fetchall()
        current_match = []
        for row in event:
            current_match.append(dict(row))
        return current_match