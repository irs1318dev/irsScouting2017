import csv
import os
import db

from sqlalchemy.sql import text




def loadGameSheet():
    fpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(fpath)
    file = open('game_sheet.csv')
    sheet = csv.reader(file)
    # writer = csv.DictWriter(sheet, fieldnames=["actor", "task", "claim", "auto", "teleop",
                                             #"final", "successname", "missname", "enums"], delimitor=',')
    # writer.writeheader()
    for row in sheet:
        insertgame(row[0],row[1],row[2],row[3],row[4],row[5])


def insertgame(actor, task, claim, auto, teleop, final):
    engine = db.getdbengine()
    conn = engine.connect()
    select = text(
        "INSERT INTO games (actor, task, claim, auto, teleop, final) " +
        "VALUES (:actor,:task,:claim,:auto,:teleop,:final); "
    )
    conn.execute(select, actor=actor, task=task, claim=claim, auto=auto, teleop=teleop, final=final)


