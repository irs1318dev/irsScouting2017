import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def game(self):
        with open("TestJson/layout", "r") as json:
            return json.read()

    @cherrypy.expose
    def match(self):
        with open("TestJson/match", "r") as json:
            return json.read()

if __name__ == '__main__':
    cherrypy.config.update(
        {'server.socket_host': '0.0.0.0'})
    cherrypy.quickstart(HelloWorld())
