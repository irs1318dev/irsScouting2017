import os.path

import pandas as pd
from sqlalchemy import text

import server.model
from server.model import event as event


def measure_summary_df(num_matches=12):
    # Connect to database
    engine = server.model.connection.engine
    conn = engine.connect()

    # Get current event
    evt_id = event.EventDal.get_current_event()[0]

    select_sum = text(
        "with current AS (SELECT status.event_id as event_id, status.match, date from schedules sched, "
        "status WHERE sched.event_id = status.event_id "
        "AND sched.match = status.match limit 1), "

        "recent_matches as ( SELECT * FROM ( "
        "SELECT row_number() over (partition by team order by sched.date desc) as r, "
        " sched.* from schedules sched, current c WHERE sched.event_id = c.event_id and sched.date <= c.date )"
        " row_schedule WHERE row_schedule.r <= " + str(
            num_matches) + " ORDER by team, date desc), "

       "team_match_count as ( "
       "select team, count(team) as team_matches from recent_matches group by team"
       ") "

       "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, actors.name AS actor, "
       "MAX(team_match_count.team_matches) AS matches, "
       "SUM(successes) AS sum_successes, MAX(successes) as max_successes, MIN(successes) as min_successes, "
       "COUNT(successes) AS count_successes, AVG(successes) as avg_successes, "
       "SUM(attempts) AS sum_attempts, MAX(attempts) as max_attempts, MIN(attempts) AS min_attempts, "
       "COUNT(attempts) AS count_attempts, AVG(attempts) as avg_attempts, "
       "MAX(cycle_times) AS max_cycle_times, MIN(cycle_times) AS min_cycle_times, "
       "AVG(cycle_times), COUNT(cycle_times) AS count_cycle_times "
       "FROM ((((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
       "LEFT JOIN tasks ON tasks.id = measures.task_id) "
       "LEFT JOIN phases ON phases.id = measures.phase_id) "
       "LEFT JOIN events ON events.id = measures.event_id) "
       "LEFT JOIN actors ON actors.id = measures.actor_id "
       "LEFT JOIN matches ON matches.id = measures.match_id "
       "LEFT JOIN team_match_count ON team_match_count.team = teams.name "
       "RIGHT JOIN recent_matches ON recent_matches.match = matches.name AND team_match_count.team = teams.name "
       "AND recent_matches.team = team_match_count.team "
       "WHERE events.id = " + str(evt_id) + " AND actors.name<> 'alliance' "
       "GROUP BY teams.name, tasks.name, phases.name, actors.name "
       "ORDER BY teams.name, phases.name, tasks.name, actors.name;"
    )
    summ_df = pd.read_sql(select_sum, conn)
    summ_df.set_index(['team', 'phase', 'actor', 'task'], inplace=True)
    return summ_df


def ranking_df(num_matches):
    summ_df = measure_summary_df(num_matches)
    rank_df = summ_df.stack()
    rank_stacked_df = rank_df.unstack([1, 2, 3, 4])
    return rank_stacked_df.sort_index(axis= 1, level= [0,1,2])


def get_rankings_old(name=None, tasks=None, num_matches=12):
    # Connect to database
    engine = server.model.connection.engine
    conn = engine.connect()

    # Get current event
    evt_id = event.EventDal.get_current_event()[0]

    select_sum = text(
        "with current AS (SELECT status.event_id as event_id, status.match, date from schedules sched, "
        "status WHERE sched.event_id = status.event_id "
        "AND sched.match = status.match limit 1), "

        "recent_matches as ( SELECT * FROM ( "
        "SELECT row_number() over (partition by team order by sched.date desc) as r, "
        " sched.* from schedules sched, current c WHERE sched.event_id = c.event_id and sched.date <= c.date )"
        " row_schedule WHERE row_schedule.r <= " + str(
            num_matches) + " ORDER by team, date desc), "

       "team_match_count as ( "
       "select team, count(team) as team_matches from recent_matches group by team"
       ") "

       "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, actors.name AS actor, "
       "MAX(team_match_count.team_matches) AS matches, "
       "SUM(successes) AS sum_successes, MAX(successes) as max_successes, MIN(successes) as min_successes, "
       "COUNT(successes) AS count_successes, AVG(successes) as avg_successes, "
       "SUM(attempts) AS sum_attempts, MAX(attempts) as max_attempts, MIN(attempts) AS min_attempts, "
       "COUNT(attempts) AS count_attempts, AVG(attempts) as avg_attempts, "
       "MAX(cycle_times) AS max_cycle_times, MIN(cycle_times) AS min_cycle_times, "
       "AVG(cycle_times), COUNT(cycle_times) AS count_cycle_times "
       "FROM ((((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
       "LEFT JOIN tasks ON tasks.id = measures.task_id) "
       "LEFT JOIN phases ON phases.id = measures.phase_id) "
       "LEFT JOIN events ON events.id = measures.event_id) "
       "LEFT JOIN actors ON actors.id = measures.actor_id "
       "LEFT JOIN matches ON matches.id = measures.match_id "
       "LEFT JOIN team_match_count ON team_match_count.team = teams.name "
       "RIGHT JOIN recent_matches ON recent_matches.match = matches.name AND team_match_count.team = teams.name "
       "AND recent_matches.team = team_match_count.team "
       "WHERE events.id = " + str(evt_id) + " AND actors.name<> 'alliance' "
       "GROUP BY teams.name, tasks.name, phases.name, actors.name "
       "ORDER BY teams.name, phases.name, tasks.name, actors.name;"
    )
    df = pd.read_sql(select_sum, conn)

    # tms_sql = text(
    #     "with current AS (SELECT s.match, date from schedules sched, "
    #     "status s WHERE sched.event = s.event "
    #     "AND sched.match = s.match limit 1 ), "
    #     "recent_matches as ( SELECT * FROM ( "
    #     "SELECT row_number() over (partition by team order by sched.date desc) as r, "
    #     " sched.* from schedules sched, current c WHERE sched.date <= c.date )"
    #     " row_schedule WHERE row_schedule.r <= " + str(num_matches) + " ORDER by team, date desc) "
    #     "SELECT team, COUNT(team) AS team_matches FROM recent_matches "
    #     "GROUP BY team;")
    # df_num_matches = pd.read_sql(tms_sql, conn)


    # index = pd.MultiIndex.from_tuples([('summary', 'robot', 'matches')])
    # df_num_matches = pd.DataFrame(df_num_matches, columns = [index, 'team', 'recent_matches'])
    # print(df_num_matches)
    #df_num_matches = df_num_matches.set_index('team')

    if tasks is not None:
        df = df[df['task'].isin(tasks)]

    # Extract each task into it's own column and sort
    # df_team_matches = pd.concat([df.loc[:, ['team', 'matches']], df_team_matches.team.unique()], axis = 1)
    # df_team_matches = df_team_matches.set_index(['team']).unique()
    # print df_team_matches #DEBUG:
    # del df['matches']
    df_indexed = df.set_index(['team', 'phase', 'actor', 'task'])
    df_stack = df_indexed.stack()
    df_unstacked = df_stack.unstack([1, 2, 3, 4])
    df_unstacked = df_unstacked.sort_index(axis= 1, level= [0,1,2])

    # For every task, add a percent column
    for col in df_unstacked:
        if col[3] == 'sum_successes':
            phase = col[0]
            actor = col[1]
            task = col[2]
            percent = df_unstacked[(phase, actor, task, 'sum_successes')] /\
                      df_unstacked[(phase, actor, task, 'sum_attempts')]
            df_unstacked.insert(0, (phase, actor, task, 'percent'), percent)
            df_unstacked = df_unstacked.sort_index(axis = 1, level = [0,1,2])

    # Average select statement
    select_avg = text(
            "SELECT schedules.team AS team, phases.name AS phase, "
            "tasks.name AS task, actors.name AS actor, "
            "AVG(measures.successes) AS avg_successes, "
            "AVG(measures.attempts) AS avg_attempts "
            "FROM measures LEFT JOIN matches ON measures.match_id=matches.id "
            "LEFT JOIN alliances ON measures.alliance_id=alliances.id "
            "LEFT JOIN schedules ON matches.name=schedules.match AND "
            "alliances.name=schedules.alliance "
            "LEFT JOIN stations ON measures.station_id=stations.id "
            "LEFT JOIN tasks ON measures.task_id=tasks.id "
            "LEFT JOIN events ON measures.event_id=events.id "
            "LEFT JOIN actors ON measures.actor_id=actors.id "
            "LEFT JOIN phases ON measures.phase_id=phases.id "
            "WHERE events.id = " + evt_id + " AND actors.name='alliance' "
            "GROUP BY schedules.team, phases.name, tasks.name, actors.name "
            "ORDER BY tasks.name, schedules.team;")

    df_avg = pd.read_sql(select_avg, conn)

    if tasks is not None:
        df_avg = df_avg[df_avg['task'].isin(tasks)]

    df_avg_index = df_avg.set_index(['team', 'phase', 'actor', 'task'])
    df_avg_stack = df_avg_index.stack()
    df_avg_unstacked = df_avg_stack.unstack([1, 2, 3, 4])
    df_avg_unstacked = df_avg_unstacked.sort_index(axis=1, level=[0, 1, 2])

    # merging summary and average dataframes
    df_joined = pd.concat([df_unstacked, df_avg_unstacked], axis=1)
    df_joined = df_joined.sort_index(axis=1, level=[0, 1, 2])

    # Save to Excel
    if name is not None:
        name = os.path.abspath(name)
        df_joined.to_excel(name, "All")

    return df_joined