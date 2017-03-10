import db
import os

engine = db.getdbengine()
conn = engine.connect()


class ExportCSV(object):

    @staticmethod
    def single(table):
        path = 'Data/' + table + '.csv'
        open(path, 'w')

        path = os.path.abspath(path)
        sql = "COPY " + table + " TO '" + path + "' CSV HEADER;"

        conn.execute(sql)

    @staticmethod
    def alltables():
        ExportCSV.single('measures')
        ExportCSV.single('tasks')
        ExportCSV.single('schedules')
        ExportCSV.single('teams')
        ExportCSV.single('matches')
        ExportCSV.single('dates')
        ExportCSV.single('events')
        ExportCSV.single('levels')
        ExportCSV.single('alliances')
        ExportCSV.single('stations')
        ExportCSV.single('actors')
        ExportCSV.single('phases')
        ExportCSV.single('measuretypes')
        ExportCSV.single('attempts')
        ExportCSV.single('reasons')
        ExportCSV.single('games')
        ExportCSV.single('task_options')
        ExportCSV.single('status')

