import os.path

import pandas
import sqlalchemy

import server.model.connection as sm_connection
import server.model.event as sm_event
from server.model import event as event


def match_num_df(num_matches=12):
    conn = sm_connection.engine.connect()
    evt_id = event.EventDal.get_current_event()[0]

    matches_sql = sqlalchemy.text(
        "WITH current AS "
        "(SELECT status.event_id as event_id, status.match, schedules.date "
        "FROM status INNER JOIN schedules "
        "ON status.event_id=schedules.event_id AND "
        "status.match=schedules.match "
        "WHERE date <> 'na' LIMIT 1), "

        "recent_matches as "
        "(SELECT * FROM ( "
        "SELECT row_number() "
        "over (partition by team order by sched.date desc) as r, "
        " sched.* from schedules sched, current c "
        "WHERE sched.event_id = c.event_id and sched.date <= c.date )"
        " row_schedule "
        "WHERE row_schedule.r <= :num_mtchs ORDER by team, date desc), "
        "team_match_count as ( "
        "select team, count(team) as team_matches from recent_matches group by team"
        ") "
        "SELECT team, MAX(r) AS matches FROM recent_matches GROUP BY team ORDER BY team;"
    ).bindparams(num_mtchs=num_matches)
    matches_df = pandas.read_sql(matches_sql, conn)
    conn.close()
    return matches_df


def measure_summary_df(num_matches=12):
    # Connect to database
    conn = sm_connection.engine.connect()

    # Get current event
    evt_id = event.EventDal.get_current_event()[0]

    select_sum = sqlalchemy.text(
        "WITH current AS "
        "(SELECT status.event_id as event_id, status.match, schedules.date "
        "FROM status INNER JOIN schedules "
        "ON status.event_id=schedules.event_id AND "
        "status.match=schedules.match "
        "WHERE date <> 'na' LIMIT 1), "

        "recent_matches as "
        "(SELECT * FROM ( "
        "SELECT row_number() "
        "over (partition by team order by sched.date desc) as r, "
        " sched.* from schedules sched, current c "
        "WHERE sched.event_id = c.event_id and sched.date <= c.date )"
        " row_schedule "
        "WHERE row_schedule.r <= " + str(
            num_matches) + " ORDER by team, date desc), "

        "team_match_count as ( "
        "SELECT team, count(team) AS team_matches FROM recent_matches "
        "GROUP BY team) "
        
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task,"
        "actors.name AS actor, "
        "MAX(team_match_count.team_matches) AS matches, "
        
        "SUM(successes) AS sum_successes, MAX(successes) as max_successes, "
        "MIN(successes) AS min_successes, COUNT(successes) AS count_successes, "
        "CAST(SUM(successes) AS FLOAT)/MAX(team_match_count.team_matches) AS avg_successes, "
        "AVG(successes) AS tav_successes, "
        
        "SUM(attempts) AS sum_attempts, MAX(attempts) as max_attempts, "
        "MIN(attempts) AS min_attempts, COUNT(attempts) AS count_attempts, "
        "CAST(SUM(attempts) AS FLOAT)/MAX(team_match_count.team_matches) as avg_attempts, "
        "AVG(attempts) AS tav_attempts, "
        
        "SUM(cycle_times) AS sum_cycle_times,"
        "MAX(cycle_times) AS max_cycle_times, "
        "MIN(cycle_times) AS min_cycle_times, "
        "CAST(SUM(cycle_times) AS FLOAT)/MAX(team_match_count.team_matches) AS avg_cycle_times, "
        "AVG(cycle_times) AS tav_cycle_times, "
        "COUNT(cycle_times) AS count_cycle_times, "
        
        "SUM(capability) AS sum_capabilities, "
        "MAX(capability) as max_capabilities, "
        "MIN(capability) AS min_capabilities, "
        "COUNT(capability) AS count_capabilities, "
        "CAST(SUM(capability) AS FLOAT)/MAX(team_match_count.team_matches) as avg_capabilities, "
        "AVG(capability) AS tav_capabilities "
        
        "FROM (((((((teams FULL OUTER JOIN measures "
        "ON teams.id=measures.team_id) "
        "LEFT JOIN tasks ON tasks.id = measures.task_id) "
        "LEFT JOIN phases ON phases.id = measures.phase_id) "
        "LEFT JOIN events ON events.id = measures.event_id) "
        "LEFT JOIN actors ON actors.id = measures.actor_id) "
        "LEFT JOIN matches ON matches.id = measures.match_id) "
        "LEFT JOIN team_match_count ON team_match_count.team = teams.name) "
        "RIGHT JOIN recent_matches ON recent_matches.match = matches.name AND "
        "team_match_count.team = teams.name "
        "AND recent_matches.team = team_match_count.team "
        "WHERE events.id = :evt_id "
        "GROUP BY teams.name, tasks.name, phases.name, actors.name "
        "ORDER BY teams.name, phases.name, tasks.name, actors.name;"
    ).bindparams(evt_id=evt_id)
    summ_df = pandas.read_sql(select_sum, conn)
    summ_df.set_index(['team', 'phase', 'actor', 'task'], inplace=True)
    conn.close()
    return summ_df


def ranking_df(num_matches):
    summ_df = measure_summary_df(num_matches)
    rank_df = summ_df.stack()
    rank_stacked_df = rank_df.unstack([1, 2, 3, 4])
    return rank_stacked_df.sort_index(axis= 1, level= [0,1,2])


def events_df():
    conn = sm_connection.engine.connect()
    sql = sqlalchemy.text(
        "SELECT events.*, event_data.measure_count FROM events LEFT JOIN ("
        "     SELECT COUNT(measures.task_id) AS measure_count, "
        "     measures.event_id AS event_id"
        "     FROM measures "
        "     GROUP BY measures.event_id) AS event_data "
        "ON events.id = event_data.event_id;")
    df = pandas.read_sql(sql, conn)
    conn.close()
    return df
