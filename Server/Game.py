import json


class Measure(object):
    def __init__(self, match, team, task, success, miss):
        self.match = match
        self.team = team
        self.taskId = task
        self.success = success
        self.miss = miss


class HelloWorld(object):
    @staticmethod
    def game():
        with open("TestJson/layout", "r") as text:
            return text.read()

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

        with open("TestJson/layout", "r") as text:
            for line in text:
                if '''"id":''' + str(task) in line:
                    for value in line.split(','):
                        if 'page' in value:
                            m.page = value.split(':')[1].replace('"', '')
            out = json.dumps(m, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)

            for value in out.split(','):
                if m.page not in value:
                    out = out.replace(value, value.split(':')[0] + ':' + value.split(':')[1].replace('"', ''))

            with open("TestJson/measures", "a") as new:
                new.write('\n' + out)

