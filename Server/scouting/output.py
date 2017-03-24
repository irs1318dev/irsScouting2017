import db
import event
from sqlalchemy.sql import text
import pandas as pd
import Tkinter
import datetime
import tkFileDialog
from collections import OrderedDict

def get_rankings(tasks = None, excel_file = 'Rankings'):
    # Connect to database
    engine = db.getdbengine()
    conn = engine.connect()

    # Get current event
    evt = event.EventDal.get_current_event()

    # Retrieve sums of succcesses and attempts columns from measures table.
    select_sum = text(
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, actors.name AS actor, "
        "SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts "
        "FROM ((((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
        "LEFT JOIN tasks ON tasks.id = measures.task_id) "
        "LEFT JOIN phases ON phases.id = measures.phase_id) "
        "LEFT JOIN events ON events.id = measures.event_id) "
        "LEFT JOIN actors ON actors.id = measures.actor_id "
        "WHERE events.name = '" + evt + "' AND actors.name<> 'alliance' "
        "GROUP BY teams.name, tasks.name, phases.name, actors.name "
        "ORDER BY teams.name, phases.name, tasks.name, actors.name;")
    df = pd.read_sql(select_sum, conn)

    if tasks is not None:
        df = df[df['task'].isin(tasks)]

    # Extract each task into it's own column and sort
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

    print df_avg.head()  # debug
    df_avg_index = df_avg.set_index(['team', 'phase', 'actor', 'task'])
    df_avg_stack = df_avg_index.stack()
    df_avg_unstacked = df_avg_stack.unstack([1, 2, 3, 4])
    df_avg_unstacked = df_avg_unstacked.sort_index(axis=1, level=[0, 1, 2])
    print df_avg_unstacked # debug

    # merging summary and average dataframes
    df_joined = pd.concat([df_unstacked, df_avg_unstacked], axis=1)
    df_joined = df_joined.sort_index(axis=1, level=[0, 1, 2])

    # Save to Excel
    if excel_file is not None:
        # Create timestamp for filename
        ts = datetime.datetime.now().strftime("%Y%b%d_%H%M%S")
        fname = excel_file + '_' + evt + ts + '.xlsx'

        # Display save-as file dialog.
        root = Tkinter.Tk()
        file_path =  tkFileDialog.asksaveasfilename(defaultextension = 'xlsx',
                title = "Save Rankings File", initialfile = fname,
                                                    parent = root)
        df_joined.to_excel(file_path, "All")
        root.destroy() # Necessary for closing tkinter window.

    #return df_all

def get_Basic_Ranking():
    get_rankings(['moveBaseline', 'placeGear','shootHighBoiler',
                  'shootLowBoiler'])


