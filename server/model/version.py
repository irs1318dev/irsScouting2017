import sqlalchemy as sa
import server.model.connection as smc

# scouting system run at houston 2017 is version 2017.01

def set_ver_2018_01():
    """Updates scouting system to version 2018.01

    Adds columns season and ver to events and status tables respectively
    Use to update from 2017.01
    """
    conn = smc.engine.connect()
    select = sa.text("ALTER TABLE events ADD COLUMN season varchar(4);")
    conn.execute(select)
    select = sa.text("UPDATE events SET season = 2017;")
    conn.execute(select)
    select = sa.text("ALTER TABLE status ADD COLUMN ver varchar(7);")
    conn.execute(select)
    select = sa.text("UPDATE status SET ver = 2018.01")
    conn.execute(select)
    conn.close()
