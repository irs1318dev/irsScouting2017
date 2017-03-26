import db
import os
import datetime

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


class ExportBackup(object):

    @staticmethod
    def runBackup(event):
        name = event + datetime.datetime.now().strftime('_%Y_%m%d_%H%M')
        return '"C:/Program Files/PostgreSQL/9.6/bin/pg_dump" -U irs1318 scouting > Desktop/' + name
