import warnings

import sqlalchemy
import sqlalchemy.exc

import server.model.connection as smc

# scouting system run at houston 2017 is version 2017.01
def get_version():
    conn = smc.engine.connect()
    sql = sqlalchemy.text("SELECT ver FROM status;")
    version = None
    try:
        version = conn.execute(sql).scalar()
    except sqlalchemy.exc.ProgrammingError:
        warnings.warn("Your scouting system schema has not been updated. Run "
                      "the 'set_ver' functions in server.model.version.")
    finally:
        conn.close()
    return version


def set_ver_2018_01():
    """Updates scouting system to version 2018.01

    Adds columns season and ver to events and status tables respectively
    Use to update from 2017.01
    """
    conn = smc.engine.connect()
    select = sqlalchemy.text("ALTER TABLE events ADD COLUMN season varchar(4);")
    conn.execute(select)
    select = sqlalchemy.text("UPDATE events SET season = 2017;")
    conn.execute(select)
    select = sqlalchemy.text("ALTER TABLE status ADD COLUMN ver varchar(7);")
    conn.execute(select)
    select = sqlalchemy.text("UPDATE status SET ver = 2018.01")
    conn.execute(select)
    conn.close()


def set_ver_2018_02():
    """Updates scouting system to version 2018.02

    Replaces event column in status table with event_id column.
    """
    if get_version() != "2018.01":
        warnings.warn("You must update the scouting schema to 2018.01 before "
                      "running this function.")
        return
    conn = smc.engine.connect()
    sql = sqlalchemy.text("ALTER TABLE status ADD COLUMN event_id integer;")
    conn.execute(sql)
    sql = sqlalchemy.text("ALTER TABLE status DROP COLUMN event")
    conn.execute(sql)
    sql = sqlalchemy.text("ALTER TABLE events DROP CONSTRAINT events_name_key;")
    conn.execute(sql)
    sql = sqlalchemy.text("UPDATE status SET ver = 2018.02")
    conn.execute(sql)
    conn.close()
