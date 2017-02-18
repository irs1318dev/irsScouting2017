import json


class Measure(object):
    def __init__(self, match, team, task, success, miss):
        self.match = match
        self.team = team
        self.taskId = task
        self.success = success
        self.miss = miss


class Task(object):
    def __init__(self, line):
        value = line.split(',')
        self.id = value[0]
        self.task = value[1]
        self.actor = value[2]
        self.page = value[3]
        self.format = value[4]
        self.success = value[5]
        self.miss = value[6]
        self.compacting = value[7].lower()
        self.newpart = value[8].lower()
        self.additions = value[9]


class HelloWorld(object):
    @staticmethod
    def game():
        with open("TestJson/newLayout.csv", "r") as text:
            out = ''
            for line in text:
                task = Task(line)
                data = json.dumps(task, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)

                for value in data.split(','):
                    if 'id' in value or 'compacting' in value or 'newpart' in value:
                        data = data.replace(value, value.split(':')[0] + ':' + value.split(':')[1].replace('"', ''))

                out += data + '\n'
            return out

    @staticmethod
    def match(number):
        with open("TestJson/match", "r") as text:
            out = ""
            for line in text:
                if '''"number":''' + str(number) in line:
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
            return out + 'end'

    @staticmethod
    def data(match, team, task, success, miss):
        m = Measure(match, team, task, success, miss)

        with open("TestJson/newLayout.csv", "r") as text:
            for line in text:
                if m.taskId in line.split(',')[0]:
                    m.page = line.split(',')[3]
            out = json.dumps(m, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)

            for value in out.split(','):
                if m.page not in value:
                    out = out.replace(value, value.split(':')[0] + ':' + value.split(':')[1].replace('"', ''))

            with open("TestJson/measures", "a") as new:
                new.write('\n' + out)

