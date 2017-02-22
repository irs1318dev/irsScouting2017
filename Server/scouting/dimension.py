
import psycopg2.extras

conn = psycopg2.connect("dbname=scouting host=localhost user=postgres password=irs1318")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def find_id(table):
    nameToId = {}
    idToName = {}

    cur.execute("SELECT id, name FROM " + table)
    res = cur.fetchall()
    for row in res:
        rowDict = dict(row)
        nameToId[rowDict['name']] = rowDict['id']
        idToName[rowDict['id']] = rowDict['name']
    return nameToId, idToName