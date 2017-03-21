import db
import os
import time
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
    def getTimeStamp():
        ts = time.time()
        time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m%d-%H%M')
        return time

    @staticmethod
    def runBackup(event):


