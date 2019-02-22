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
    sql = sqlalchemy.text("ALTER TABLE events "
                          "ADD CONSTRAINT events_unique UNIQUE (name, season);")
    conn.execute(sql)
    sql = sqlalchemy.text("UPDATE status SET ver = 2018.02")
    conn.execute(sql)
    conn.close()


def set_ver_2018_03():
    """Modifies schedules table to use event_id as foreign key.
    """
    if get_version() != "2018.02":
        warnings.warn("You must update the scouting schema to 2018.02 before "
                      "running this function.")
        return
    conn = smc.engine.connect()
    trans = conn.begin()
    try:
        sql = sqlalchemy.text("ALTER TABLE schedules "
                              "ADD COLUMN event_id integer;")
        conn.execute(sql)
        sql = sqlalchemy.text("SELECT DISTINCT event FROM schedules;")
        sched_events = conn.execute(sql)
        for event in sched_events:
            sql = sqlalchemy.text("SELECT id FROM events WHERE name = :evt")
            evt_id = conn.execute(sql, evt=event["event"]).scalar()
            sql = sqlalchemy.text("UPDATE schedules SET event_id = :id "
                                  "WHERE event = :evt;")
            conn.execute(sql, id=evt_id, evt=event["event"])
        sql = sqlalchemy.text("ALTER TABLE schedules DROP COLUMN event;")
        conn.execute(sql)
        sql = sqlalchemy.text("UPDATE status SET ver = 2018.03;")
        conn.execute(sql)
        trans.commit()
    except:
        trans.rollback()
        print("\n======ERROR: SQL Transactions did not run=========")
        raise
    else:
        print("\n==========SUCCESS!==========")
    finally:
        conn.close()


def set_ver_2019_01():
    conn = smc.pool.getconn()
    sql1 = '''
        CREATE OR REPLACE VIEW vw_status_date AS 
        SELECT status.event_id AS event_id, status.match, schedules.date
        FROM status INNER JOIN schedules
            ON  status.event_id=schedules.event_id AND
                    status.match=schedules.match
        WHERE date <> 'na' LIMIT 1;
    '''
    curr = conn.cursor()
    curr.execute(sql1)
    sql = '''
        CREATE OR REPLACE VIEW vw_schedule AS
        SELECT * FROM (
            SELECT
                row_number() OVER (
                    PARTITION BY team ORDER BY sched.date DESC) AS last_match,
                sched.*
            FROM schedules AS sched, vw_status_date AS c
            WHERE sched.event_id = c.event_id AND sched.date <= c.date)
        AS row_schedule
        ORDER BY date DESC;
    '''
    curr.execute(sql)
    sql = '''
        CREATE OR REPLACE VIEW vw_measures AS
        SELECT dates.name AS date, events.name AS event,
                events.season AS season, levels.name AS level,
                matches.name AS match, alliances.name AS alliance,
                teams.name AS team, stations.name AS station,
                actors.name AS actor, tasks.name AS task,
                measuretypes.name AS measuretype, phases.name AS phase,
                attempts.name AS attempt,reasons.name AS reason, 
                task_options.option_name AS capability, measures.successes,
                measures.attempts, measures.cycle_times, 
                vw_schedule.last_match AS last_match, MAX(last_match) OVER (PARTITION BY team) AS num_matches
        FROM ((((((((((((((measures
            LEFT JOIN task_options ON measures.capability=task_options.id)
            INNER JOIN dates ON measures.date_id=dates.id)
            INNER JOIN events ON measures.event_id=events.id)
            INNER JOIN levels ON measures.level_id=levels.id)
            INNER JOIN matches ON measures.match_id=matches.id)
            INNER JOIN alliances ON measures.alliance_id=alliances.id)
            INNER JOIN teams ON measures.team_id=teams.id)
            INNER JOIN stations ON measures.station_id=stations.id)
            INNER JOIN actors ON measures.actor_id=actors.id)
            INNER JOIN tasks ON measures.task_id=tasks.id)
            INNER JOIN measuretypes ON measures.measuretype_id=measuretypes.id)
            INNER JOIN phases ON measures.phase_id=phases.id)
            INNER JOIN attempts ON measures.attempt_id=attempts.id)
            INNER JOIN reasons ON measures.reason_id=reasons.id)
            INNER JOIN vw_schedule ON teams.name=vw_schedule.team AND
                       matches.name=vw_schedule.match
            WHERE measures.event_id=vw_schedule.event_id; 
    '''
    curr.execute(sql)

    sql = '''
    CREATE OR REPLACE VIEW vw_num_matches AS
    SELECT team, MAX(last_match) AS matches
            FROM vw_schedule
            GROUP BY team ORDER BY team;
    '''
    curr.execute(sql)
    sql = '''UPDATE status SET ver = 2019.01;'''
    curr.execute(sql)
    conn.commit()
    curr.close()