import scouting.db as db
import os
import datetime
import subprocess

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
    def all_tables():
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
    def run_backup(event):
        name = event + datetime.datetime.now().strftime('_%Y_%m%d_%H%M')
        command = ['pg_dump', '-U', 'irs1318', 'scouting']

        subprocess.call(command, stdout=open('web/data/' + name, 'w'))
        return name

    @staticmethod
    def run_restore(path):
        command = ['pgsql', '-U', 'irs1318', 'scouting']

        subprocess.call(command, stdin=open(path))
