import db
from sqlalchemy.sql import text



def add_name(table, col, val):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO " + table + " (" + col + ") " +
        "VALUES (:val) "
        "ON CONFLICT " + "(" + col + ")" +
        " DO UPDATE "
        "SET " + col + " = :val RETURNING id; "
    )
    conn.execute(select, val=val)


def add_many_names(table, col, n, template):
    engine = db.getdbengine()
    conn = engine.connect()
    for i in range(1, n):
        name = template.format(i)
        sql = text(
            "INSERT INTO " + table + " (" + col + ") " +
            "VALUES (:name) "
            "ON CONFLICT (" + col + ") " +
            "DO UPDATE "
            "SET " + col + " = :name RETURNING id; "

        )
        conn.execute(sql, name=name)

# This function does not yet work -- don't use it. Check with Stacy if you
# have questions.
def add_many_cols(table, cols, vals) :
    engine = db.getdbengine()
    conn = engine.connect()

    # Buld string containing column names
    col_names = ""
    for col in cols:
        if col_names == "":
            col_names = col
        else:
            col_names = col_names + ", " + col

    sql = text(
        "INSERT INTO " + table + " (" + col_names + ") " +
        "VALUES (:name)"
    ).params(vals)
    conn.execute(sql)


def insertData():
    add_name("levels", "name", "qual")
    add_name("levels", "name", "playoff")

    add_many_names("matches", "name", 150, "{0:0>3}-q")
    add_name("matches", "name", "q1.1")
    add_name("matches", "name", "q1.2")
    add_name("matches", "name", "q1.3")
    add_name("matches", "name", "q2.1")
    add_name("matches", "name", "q2.2")
    add_name("matches", "name", "q2.3")
    add_name("matches", "name", "q3.1")
    add_name("matches", "name", "q3.2")
    add_name("matches", "name", "q3.3")
    add_name("matches", "name", "s1.1")
    add_name("matches", "name", "s1.2")
    add_name("matches", "name", "s1.3")
    add_name("matches", "name", "s2.1")
    add_name("matches", "name", "s2.2")
    add_name("matches", "name", "s2.3")
    add_name("matches", "name", "f1")
    add_name("matches", "name", "f2")
    add_name("matches", "name", "f3")
    add_name("matches", "name", "pit")

    add_name("alliances", "name", "na")
    add_name("alliances", "name", "blue")
    add_name("alliances", "name", "red")

    # teams imported from schedule

    add_name("stations", "name", "na")
    add_name("stations", "name", "1")
    add_name("stations", "name", "2")
    add_name("stations", "name", "3")

    add_name("actors", "name", "na")
    add_name("actors", "name", "drive_team")
    add_name("actors", "name", "robot")
    add_name("actors", "name", "pilot")
    add_name("actors", "name", "human_player")
    add_name("actors", "name", "alliance")
    add_name("actors", "name", "team")

    # tasks imported from game

    add_name("measuretypes", "name", "na")
    add_name("measuretypes", "name", "count")
    add_name("measuretypes", "name", "percentage")
    add_name("measuretypes", "name", "boolean")
    add_name("measuretypes", "name", "enum")
    add_name("measuretypes", "name", "attempt")
    add_name("measuretypes", "name", "cycletime")

    add_name("phases", "name", "na")
    add_name("phases", "name", "claim")
    add_name("phases", "name", "auto")
    add_name("phases", "name", "teleop")
    add_name("phases", "name", "finish")

    add_name("attempts", "name", "summary")
    add_many_names("attempts", "name", 31, "{0:0>2}")

    add_name("reasons", "name", "na")
    add_name("reasons", "name", "dropped")
    add_name("reasons", "name", "blocked")
    add_name("reasons", "name", "defended")

