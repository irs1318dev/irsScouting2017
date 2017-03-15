import db
from sqlalchemy.sql import text
import pandas as pd
import tkFileDialog
from collections import OrderedDict

def get_sum():
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts "
        "FROM ((teams FULL OUTER JOIN measures ON teams.id = measures.team_id) LEFT JOIN tasks ON tasks.id = measures.task_id) LEFT JOIN phases ON phases.id = measures.phase_id "
        " GROUP BY teams.name, tasks.name, phases.name"
        " ORDER BY teams.name, phases.name, tasks.name;")
    result_df = pd.read_sql(select, conn)

    #file_path =  tkFileDialog.asksaveasfilename(defaultextension = 'xlsx',
                                                #title = "Save Rankings File")


    #result_df.to_excel(file_path, sheet_name= 'Rankings', index = 'team')
    #del result_df['task']
    #del result_df['sum_attempts']
    #result_df = result_df.pivot(index='team')

    team_col = result_df['team'].unique()
    phases = result_df['phase'].unique()
    tasks = result_df['task'].unique()

    unstacked_table = OrderedDict()
    unstacked_table['team'] = team_col
    for phase in phases:
        for task in tasks:
            col_name = str(phase) + '_' + str(task)
            unstacked_table[col_name] = pd.Series([])
            for team in team_col:
                val = result_df.loc[(result_df['phase'] == phase) & (result_df['task'] == task) & (result_df['team'] == team)]['sum_successes']
                unstacked_table[col_name].append(val)
    print unstacked_table
