import db
from sqlalchemy.sql import text


def addname(table, col, val):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO " + table + " ("+ col+ ") " +
        "VALUES (:val) "
        "ON CONFLICT " + "(" + col + ")" +
        " DO UPDATE "
            "SET " + col +  " = :val RETURNING id; "
    )
    conn.execute(select, val = val)


def addmanyattempts(table, col, val, var):
    engine = db.getdbengine()
    conn = engine.connect()
    for i in range(1, val):
        match = var + str(i)
        select = text(
            "INSERT INTO " + table + " (" + col + ") " +
            "VALUES (:match) "
            "ON CONFLICT (" + col + ") " +
            "DO UPDATE "
                "SET " + col + " = :match RETURNING id; "

        )
        conn.execute(select, match=match)
def addmanyqual(table, col, val, var):
    engine = db.getdbengine()
    conn = engine.connect()
    for i in range(1, val):
        match = str(i) +"- " + var
        select = text(
            "INSERT INTO " + table + " (" + col + ") " +
            "VALUES (:match) "
            "ON CONFLICT (" + col + ") " +
            "DO UPDATE "
                "SET " + col + " = :match RETURNING id; "

        )
        conn.execute(select, match=match)

addname("alliances", "name", "blue")
addname("alliances", "name", "red")
addname("alliances", "name", "na")

addname("levels", "name", "qual")
addname("levels", "name", "playoff")

addname("actors", "name", "na")
addname("actors", "name", "drive_team")
addname("actors", "name", "robot")
addname("actors", "name", "pilot")
addname("actors", "name", "human_player")
addname("actors", "name", "alliance")
addname("actors", "name", "team")

addname("stations", "name", "na")
addname("stations", "name", "1")
addname("stations", "name", "2")
addname("stations", "name", "3")

addname("phases", "name", "na")
addname("phases", "name", "prep")
addname("phases", "name", "auto")
addname("phases", "name", "teleop")
addname("phases", "name", "post")

addname("reasons", "name", "na")
addname("reasons", "name", "dropped")
addname("reasons", "name", "blocked")
addname("reasons", "name", "defended")

addname("attempts", "name", "summary")
addmanyattempts("attempts", "name", 31, "attempt")

addmanyqual("matches", "name", 150, "Q")
addname("matches", "name","Q1.1")
addname("matches", "name","Q1.2")
addname("matches", "name","Q1.3")
addname("matches", "name","Q2.1")
addname("matches", "name","Q2.2")
addname("matches", "name","Q2.3")
addname("matches", "name","Q3.1")
addname("matches", "name","Q3.2")
addname("matches", "name","Q3.3")
addname("matches", "name","S1.1")
addname("matches", "name","S1.2")
addname("matches", "name","S1.3")
addname("matches", "name","S2.1")
addname("matches", "name","S2.2")
addname("matches", "name","S2.3")
addname("matches", "name","F1")
addname("matches", "name","F2")
addname("matches", "name","F3")



