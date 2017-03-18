import db
from sqlalchemy.sql import text
import pandas as pd
import tkFileDialog
from collections import OrderedDict

def get_rankings(tasks):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts "
        "FROM ((teams FULL OUTER JOIN measures ON teams.id = measures.team_id) LEFT JOIN tasks ON tasks.id = measures.task_id) LEFT JOIN phases ON phases.id = measures.phase_id "
        " GROUP BY teams.name, tasks.name, phases.name"
        " ORDER BY teams.name, phases.name, tasks.name;")
    df = pd.read_sql(select, conn)

    df = df[df['task'].isin(tasks)]
    df_indexed = df.set_index(['team', 'phase', 'task'])
    df_stack = df_indexed.stack()
    df_unstacked = df_stack.unstack([1, 2, 3])
    df_unstacked = df_unstacked.sort_index(axis= 1, level= [0,1])
    for col in df_unstacked:
        if col[2] == 'sum_successes':
            phase = col[0]
            task = col[1]
            percent = df_unstacked[(phase, task, 'sum_successes')] / df_unstacked[(phase, task, 'sum_attempts')]
            df_unstacked.insert(0, (phase, task, 'percent'), percent)
            df_unstacked = df_unstacked.sort_index(axis = 1, level = [0,1] )
    file_path =  tkFileDialog.asksaveasfilename(defaultextension = 'xlsx',
                                                title = "Save Rankings File", initialfile = 'Rankings.xlsx')
    df_unstacked.to_excel(file_path, sheet_name='Rankings')

def get_Basic_Ranking():
    get_rankings(['moveBaseline', 'placeGear','shootHighBoiler','shootLowBoiler'])


