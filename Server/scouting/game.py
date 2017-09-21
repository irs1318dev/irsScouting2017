import psycopg2.extras
from sqlalchemy import text
import scouting.db as db

# conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

engine = db.getdbengine()
conn = engine.connect()


class GameDal(object):
    # @staticmethod
    # def game(actor, measuretype):
    #     cur.execute("SELECT * FROM games WHERE "
    #                 "game = 'current' "
    #                 " AND actor = " + actor
    #                 + "AND measuretype = " + measuretype + ";")
    #     game = cur.fetchall()
    #      = []
    #     for row in game:
    #         .append(dict(row))
    #     return
    #
    @staticmethod
    def get_actor_measure(task, phase):
        sql = text("SELECT actor, " + phase + " FROM games WHERE "
                   "task = :task "
        )
        results = conn.execute(sql, task=task,phase=phase).fetchone()
        return(results)



# class EventDal(object):
#
#     @staticmethod
#     def current_match(match, team):
#         cur.execute("SELECT * FROM schedules WHERE "
#                     "match_status = 'current' "
#                     " AND team = " + team
#                     + "AND match = " + match + ";")
#         event = cur.fetchall()
#         current_match = []
#         for row in event:
#             current_match.append(dict(row))
#         return current_match