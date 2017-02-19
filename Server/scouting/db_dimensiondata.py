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

addname("alliances", "name", "blue")
addname("alliances", "name", "red")