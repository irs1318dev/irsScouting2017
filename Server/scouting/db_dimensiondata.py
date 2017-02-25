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


def add_many_names(table, col, max_val, template):
    engine = db.getdbengine()
    conn = engine.connect()
    for i in range(1, max_val):
        name = template.format(i)
        sql = text(
            "INSERT INTO " + table + " (" + col + ") " +
            "VALUES (:name) "
            "ON CONFLICT (" + col + ") " +
            "DO UPDATE "
            "SET " + col + " = :match RETURNING id; "

        )
        conn.execute(sql, name=name)


# dates imported from schedule

# events imported from schedule

add_name("levels", "name", "qual")
add_name("levels", "name", "playoff")

add_many_names("matches", "name", 150, "{}-Q")
add_name("matches", "name", "Q1.1")
add_name("matches", "name", "Q1.2")
add_name("matches", "name", "Q1.3")
add_name("matches", "name", "Q2.1")
add_name("matches", "name", "Q2.2")
add_name("matches", "name", "Q2.3")
add_name("matches", "name", "Q3.1")
add_name("matches", "name", "Q3.2")
add_name("matches", "name", "Q3.3")
add_name("matches", "name", "S1.1")
add_name("matches", "name", "S1.2")
add_name("matches", "name", "S1.3")
add_name("matches", "name", "S2.1")
add_name("matches", "name", "S2.2")
add_name("matches", "name", "S2.3")
add_name("matches", "name", "F1")
add_name("matches", "name", "F2")
add_name("matches", "name", "F3")

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
add_many_names("attempts", "name", 31, "attempt{}")

add_name("reasons", "name", "na")
add_name("reasons", "name", "dropped")
add_name("reasons", "name", "blocked")
add_name("reasons", "name", "defended")

