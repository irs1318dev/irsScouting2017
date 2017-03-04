import json
import db

engine = db.getdbengine()
conn = engine.connect()


class Task(object):
    def __init__(self, line):
        value = line.split(',')
        self.actor = value[0]
        self.task = value[1]
        self.claim = value[2]
        self.auto = value[3]
        self.teleop = value[4]
        self.finish = value[5]
        self.success = value[6]
        self.miss = value[7]
        self.enums = value[8]


class TaskDal(object):
    @staticmethod
    def gettasks():
        results = conn.execute("SELECT * FROM games")

        out = ''
        for line in results:
            task = Task(line)
            data = json.dumps(task, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)
            out += data + '\n'
        return out