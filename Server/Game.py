import cherrypy


class HelloWorld(object):
    current = 1

    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def game(self):
        with open("TestJson/layout", "r") as json:
            return json.read()

    @cherrypy.expose
    def match(self, number=current):
        with open("TestJson/match", "r") as json:
            out = ""
            for line in json:
                if """"Number":""" + str(number) in line:
                    out += line + "\n"
            return out

    @cherrypy.expose
    def matchteam(self, match=current,team=0):
        with open("TestJson/measures", "r") as json:
            out = ""
            for line in json:
                if """"Match":""" + str(match) in line:
                    if """"Team":""" + str(team) in line:
                        out += line + "\n"
            return out

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HelloWorld())
