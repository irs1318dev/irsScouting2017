import csv
import os
import os.path

import scouting.db as db
from scouting.match import MatchDal

engine = db.getdbengine()
conn = engine.connect()

def insertTestData(task, filename = "auto_test_data.csv"):
    # Change Python working directory to same as this module
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Get data from csv file -- Don't save the file in UTFi format!!!
    file = open(filename, 'rb')
    data_rdr = csv.DictReader(file)

    # Insert each row into measures column
    for row in data_rdr:
        mtch = "{0:0>3}-q".format(row['match'])
        MatchDal.matchteamtask(row['team'], task, mtch, 'auto',
                               attempt_count = 3 + int(row[task]),
                               success_count=row[task])