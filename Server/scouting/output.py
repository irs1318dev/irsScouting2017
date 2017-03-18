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
    select = text(
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, "
        "SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts "
        "FROM (((teams FULL OUTER JOIN measures ON teams.id=measures.team_id) "
        "LEFT JOIN tasks ON tasks.id = measures.task_id) "
        "LEFT JOIN phases ON phases.id = measures.phase_id) "
        "LEFT JOIN events ON events.id = measures.event_id "
        "WHERE events.name = '" + evt + "' "
        "GROUP BY teams.name, tasks.name, phases.name "
        "ORDER BY teams.name, phases.name, tasks.name;")
    df = pd.read_sql(select, conn)

    # Filter tasks based on tasks argument. If tasks omitted, return all tasks.
    if tasks is not None:
        df = df[df['task'].isin(tasks)]

    # Extract each task into it's own column and sort
    df_indexed = df.set_index(['team', 'phase', 'task'])
    df_stack = df_indexed.stack()
    df_unstacked = df_stack.unstack([1, 2, 3])
    df_unstacked = df_unstacked.sort_index(axis= 1, level= [0,1])

    # For every task, add a percent column
    for col in df_unstacked:
        if col[2] == 'sum_successes':
            phase = col[0]
            task = col[1]
            percent = df_unstacked[(phase, task, 'sum_successes')] /\
                      df_unstacked[(phase, task, 'sum_attempts')]
            df_unstacked.insert(0, (phase, task, 'percent'), percent)
            df_unstacked = df_unstacked.sort_index(axis = 1, level = [0,1] )

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
        df_unstacked.to_excel(file_path, sheet_name='Rankings')
        root.destroy() # Necessary for closing tkinter window.

    return df_unstacked

def get_Basic_Ranking():
    get_rankings(['moveBaseline', 'placeGear','shootHighBoiler',
                  'shootLowBoiler'])


