import cherrypy


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello"

    @cherrypy.expose
    def game(self):
        with open("layout.txt", "r") as json:
            return json.read()


if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
