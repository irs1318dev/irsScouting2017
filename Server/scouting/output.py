import db
from sqlalchemy.sql import text
import pandas
import tkFileDialog
import xlsxwriter



def get_sum():
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "SELECT teams.name AS team, phases.name AS phase, tasks.name AS task, SUM(successes) AS sum_successes, SUM(attempts) AS sum_attempts "
        "FROM ((teams FULL OUTER JOIN measures ON teams.id = measures.team_id) LEFT JOIN tasks ON tasks.id = measures.task_id) LEFT JOIN phases ON phases.id = measures.phase_id "
        " GROUP BY teams.name, tasks.name, phases.name"
        " ORDER BY teams.name, phases.name, tasks.name;")
    result_df = pandas.read_sql(select, conn)

    file_path =  tkFileDialog.asksaveasfile()
    workbook = xlsxwriter.Workbook(file_path)

    result_df.to_excel(workbook, sheet_name= 'Rankings')

#get_sum("climbRope", "teleop", "success")
#get_sum("placeGear", "auto", "attempt")


