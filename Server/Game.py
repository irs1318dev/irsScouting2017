import cherrypy
import json


class Measure(object):
    def __init__(self, match, team, task, success, miss):
        self.match = match
        self.team = team
        self.taskId = task
        self.success = success
        self.miss = miss


class HelloWorld(object):
    current = 1

    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def game(self):
        with open("TestJson/layout", "r") as text:
            return text.read()

    @cherrypy.expose
    def match(self, number=current):
        with open("TestJson/match", "r") as text:
            out = ""
            for line in text:
                if '''"number":''' + str(number) in line:
                    out += line
            return out

    @cherrypy.expose
    def matchteam(self, match=current, team=0):
        with open("TestJson/matchteam", "r") as text:
            out = ""
            for line in text:
                if '"match":' + str(match) in line:
                    if '"team":' + str(team) in line:
                        out += line
            return out

    @cherrypy.expose
    def data(self, match=current, team=-1, task=-1, success=0, miss=0):
        m = Measure(match, team, task, success, miss)

        if not task == -1 and not team == -1:
            with open("TestJson/layout", "r") as text:
                for line in text:
                    if '''''''"id":''' + str(task) in line:
                        for value in line.split(','):
                            if 'page' in value:
                                m.page = value.split(':')[1].replace('"', '')
            out = json.dumps(m, default=lambda o: o.__dict__, separators=(', ', ':'), sort_keys=True)

            for value in out.split(','):
                if 'taskId' in value or 'team' in value or 'success' in value:
                    out = out.replace(value, value.split(':')[0] + ':' + value.split(':')[1].replace('"', ''))

            with open("TestJson/matchteam", "a") as text:
                text.write('\n' + out)

        return str(self.current)

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HelloWorld())
