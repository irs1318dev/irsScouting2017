import scouting.db as db
import os.path
import scouting.event as event
from sqlalchemy.sql import text
import pandas as pd
import datetime


def get_rankings(name=None, tasks=None, num_matches=12):
    # Connect to database
    engine = db.getdbengine()
    conn = engine.connect()

    # Get current event
    evt = event.EventDal.get_current_event()

    # Retrieve sums of succcesses and attempts columns from measures table.
    # select_sum = text(
    #     "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, actors.name AS actor, "
    #     "SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts, AVG(cycle_times) "
    #     "FROM ((((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
    #     "LEFT JOIN tasks ON tasks.id = measures.task_id) "
    #     "LEFT JOIN phases ON phases.id = measures.phase_id) "
    #     "LEFT JOIN events ON events.id = measures.event_id) "
    #     "LEFT JOIN actors ON actors.id = measures.actor_id "
    #     "WHERE events.name = '" + evt + "' AND actors.name<> 'alliance' "
    #     "GROUP BY teams.name, tasks.name, phases.name, actors.name "
    #     "ORDER BY teams.name, phases.name, tasks.name, actors.name;")
    # df = pd.read_sql(select_sum, conn)
    select_sum = text(
        "with current AS (SELECT s.event as event, s.match, date from schedules sched, "
        "status s WHERE sched.event = s.event "
        "AND sched.match = s.match limit 1 ), "

        "recent_matches as ( SELECT * FROM ( "
        "SELECT row_number() over (partition by team order by sched.date desc) as r, "
        " sched.* from schedules sched, current c WHERE sched.event = c.event and sched.date <= c.date )"
        " row_schedule WHERE row_schedule.r <= " + str(
            num_matches) + " ORDER by team, date desc), "

        "team_match_count as ( "
        "select team, count(team) as team_matches from recent_matches group by team"
           ") "

           "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, actors.name AS actor, "
           "MAX(team_match_count.team_matches) AS matches, "
           "SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts, AVG(cycle_times) "
           "FROM ((((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
           "LEFT JOIN tasks ON tasks.id = measures.task_id) "
           "LEFT JOIN phases ON phases.id = measures.phase_id) "
           "LEFT JOIN events ON events.id = measures.event_id) "
           "LEFT JOIN actors ON actors.id = measures.actor_id "
           "LEFT JOIN matches ON matches.id = measures.match_id "
           "LEFT JOIN team_match_count ON team_match_count.team = teams.name "
           "RIGHT JOIN recent_matches ON recent_matches.match = matches.name AND team_match_count.team = teams.name "
           "AND recent_matches.team = team_match_count.team "
           "WHERE events.name = '" + evt + "' AND actors.name<> 'alliance' "
           "GROUP BY teams.name, tasks.name, phases.name, actors.name "
           "ORDER BY teams.name, phases.name, tasks.name, actors.name;")
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
            "WHERE events.name = '" + evt + "' AND actors.name='alliance' "
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


def get_Basic_Ranking(name):
    return get_rankings(name, ['moveBaseline', 'placeGear', 'shootHighBoiler', 'shootLowBoiler'])


def get_Path(start):
    ts = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
    excel = start + '_' + event.EventDal.get_current_event() + ts + '.xlsx'
    return 'web/data/' + excel


def get_report(name):
    name = os.path.abspath(name)

    tasks = ['placeGear', 'shootHighBoiler', 'shootLowBoiler', 'pushTouchPad',
             'climbRope', 'defendMovement', 'moveBaseline']
    raw_df = get_rankings(None, tasks)
    final_df = pd.DataFrame()
    final_df['AutoGearMatch'] = raw_df['auto']['robot']['placeGear']['matches']
    #final_df['AutoGearAttp'] = raw_df['auto']['robot']['placeGear']['sum_attempts']
    final_df['pGearAutoAvg'] = raw_df['auto']['robot']['placeGear']['sum_successes'] / raw_df['auto']['robot']['placeGear']['matches']
    final_df['pGearAuto%'] = raw_df['auto']['robot']['placeGear']['sum_successes'] / raw_df['auto']['robot']['placeGear']['sum_attempts']

    final_df['pGearTeleAvg'] = raw_df['teleop']['robot']['placeGear']['sum_successes'] / raw_df['teleop']['robot']['placeGear']['matches']
    final_df['pGearTele%'] = raw_df['teleop']['robot']['placeGear']['sum_successes'] / raw_df['teleop']['robot']['placeGear']['sum_attempts']

    final_df['HighBoilerAutoAvg'] = raw_df['auto']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['matches']
    final_df['HighBoilerTeleAvg'] = raw_df['teleop']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['matches']

    final_df['pushTouchPad'] = raw_df['finish']['robot']['pushTouchPad']['sum_successes'] / raw_df['finish']['robot']['pushTouchPad']['matches']
    #final_df['climbRope'] = raw_df['finish']['robot']['climbRope']['sum_successes'] / raw_df['finish']['robot']['climbRope']['matches']
    final_df['defendMovement'] = raw_df['teleop']['robot']['defendMovement']['sum_successes'] / raw_df['teleop']['robot']['defendMovement']['matches']
    final_df['moveBaseline'] = raw_df['auto']['robot']['moveBaseline']['sum_successes'] / raw_df['auto']['robot']['moveBaseline']['matches']

    final_df['HighBoilerAuto%'] = raw_df['auto']['robot']['shootHighBoiler']['sum_successes'] / raw_df['auto']['robot']['shootHighBoiler']['sum_attempts']
    final_df['HighBoilerTele%'] = raw_df['teleop']['robot']['shootHighBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootHighBoiler']['sum_attempts']

    final_df['LowBoilerAuto%'] = raw_df['auto']['robot']['shootLowBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootLowBoiler']['sum_attempts']
    final_df['LowBoilerTele%'] = raw_df['teleop']['robot']['shootLowBoiler']['sum_successes'] / raw_df['teleop']['robot']['shootLowBoiler']['sum_attempts']

    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    final_df.to_excel(writer, sheet_name="All")

    # Format workbook

    wkbk = writer.book
    wksheet = writer.sheets['All']

    width = 8

    dec_format = wkbk.add_format({'num_format': '0.00'})

    #dec_format_grey = wkbk.add_format({'num_format': '0.0'})
    #dec_format_grey.set_bg_color('#D3D3D3')

    per_format = wkbk.add_format({'num_format': '0%'})

    #per_format_grey = wkbk.add_format({'num_format': '0%'})
    #per_format_grey.set_bg_color('#D3D3D3')

    int_format_grey = wkbk.add_format({'num_format': '0'})

    # wksheet.set_column('B1:B1', width, text_60)
    # wksheet.set_column('C1:C1', width, text_60)
    format = wkbk.add_format()
    format.set_rotation(70)

    name = ['AutoGearMatch','pGearAutoAvg','pGearAuto%','pGearTeleAvg','pGearTele%','HighBoilerAutoAvg',
            'HighBoilerTeleAvg','pushTouchPad','defendMovement','moveBaseline','HighBoilerAuto%','HighBoilerTele%',
             'LowBoilerAuto%','LowBoilerTele%']
    val = 1
    for i in name:
        wksheet.write(0, val,i, format)
        val = val + 1
    wksheet.set_column('B2:B100', width, int_format_grey)
    wksheet.set_column('C:C', width, dec_format)
    wksheet.set_column('D:D', width, per_format)
    wksheet.set_column('E:E', width, dec_format)
    wksheet.set_column('F:F', width, per_format)
    wksheet.set_column('G:G', width, dec_format)
    wksheet.set_column('H:H', width, dec_format)
    wksheet.set_column('I:I', width, dec_format)
    wksheet.set_column('J:J', width, dec_format)
    wksheet.set_column('K:K', width, dec_format)
    wksheet.set_column('L:L', width, per_format)
    wksheet.set_column('M:M', width, per_format)
    wksheet.set_column('N:N', width, per_format)
    wksheet.set_column('O:O', width, per_format)

    # for row in range(0, 100):
    #     if (row % 2 == 1):
    #         wksheet['C' + str(row)].style.number_format.format_code = '0.0'
    #
    #         # wksheet.set_cell(row, 'B', width, int_format_grey)
    #         # wksheet.set_cell(row, 'C', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'D', width, per_format_grey)
    #         # wksheet.set_cell(row, 'E', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'F', width, per_format_grey)
    #         # wksheet.set_cell(row, 'G', width, per_format_grey)
    #         # wksheet.set_cell(row, 'H', width, per_format_grey)
    #         # wksheet.set_cell(row, 'I', width, per_format_grey)
    #         # wksheet.set_cell(row, 'J', width, per_format_grey)
    #         # wksheet.set_cell(row, 'K', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'L', width, dec_format_grey)
    #         # wksheet.set_cell(row, 'M', width, dec_format_grey)
    #     else:
    #         pass
    #         # wksheet.set_cell(row, 'B', width, None)
    #         # wksheet.set_cell(row, 'C', width, dec_format)
    #         # wksheet.set_cell(row, 'D', width, per_format)
    #         # wksheet.set_cell(row, 'E', width, dec_format)
    #         # wksheet.set_cell(row, 'F', width, per_format)
    #         # wksheet.set_cell(row, 'G', width, per_format)
    #         # wksheet.set_cell(row, 'H', width, per_format)
    #         # wksheet.set_cell(row, 'I', width, per_format)
    #         # wksheet.set_cell(row, 'J', width, per_format)
    #         # wksheet.set_cell(row, 'K', width, dec_format)
    #         # wksheet.set_cell(row, 'L', width, dec_format)
    #         # wksheet.set_cell(row, 'M', width, dec_format)

    writer.save()



