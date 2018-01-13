import json


class Measure(object):
    def __init__(self, match, team, task, phase, value, success, miss):
        self.match = match
        self.team = team
        self.task = task
        self.phase = phase
        self.value = value
        self.success = success
        self.miss = miss


class Section(object):
    def __init__(self, line):
        value = line.split(',')
        self.actor = value[0]
        self.observer = value[1]
        self.phase = value[2]
        self.category = value[3]
        self.newpart = value[4].lower()
        self.tasks = value[5].split('|')


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


class HelloWorld(object):
    @staticmethod
    def gametasks():
        with open("Scouting/gametasks.csv", "r") as text:
            out = ''
            for line in text:
                if 'actor,task' not in line:
                    task = Task(line)
                    data = json.dumps(task, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)
                    out += data + '\n'
            return out

    @staticmethod
    def match(number):
        with open("TestJson/match", "r") as text:
            out = ""
            for line in text:
                if '''"match":"''' + str(number) in line:
                    out += line
            return out

    @staticmethod
    def matchteam(match, team):
        with open("TestJson/measures", "r") as text:
            out = ""
            for line in text:
                if '"match":' + str(match) in line:
                    if '"team":' + str(team) in line:
                        out += line
            return out

    @staticmethod
    def data(match, team, task, phase, value, success, miss):
        m = Measure(match, team, task, phase, value, success, miss)
        out = json.dumps(m, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)

        with open("TestJson/measures", "a") as new:
            new.write('\n' + out)
        return out
