import cherrypy
import random
import string

class Scouting(object):

    def __init__(self):
        self.actions = {}
        self.actions['match'] = Match()
        self.actions['event'] = Event()


    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return cherrypy.session['mystring']

    def POST(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string


    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name

class Match(object):
    @cherrypy.expose
    def index(self,vpath):
        return 'About match %s...' % (vpath.pop(0))

class Event(object):
    @cherrypy.expose
    def index(self, vpath):
        return 'About event %s...' % (vpath.pop(0))

if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        }
    }
    cherrypy.quickstart(Scouting(), '/', conf)